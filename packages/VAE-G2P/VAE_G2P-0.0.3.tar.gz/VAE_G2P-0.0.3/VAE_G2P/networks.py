import collections
import torch
from torch import nn
import math

class FixedWeights_Linear(nn.Module):

    __constants__ = ['bias', 'in_features', 'out_features']

    def __init__(self, in_features, out_features,weight_matrix, bias=True):
        """
        Modifies the Linear neural network class such that the weights are fixed and not updated during inference.
        
        """
        super(FixedWeights_Linear, self).__init__()
        self.in_features = in_features
        self.out_features = out_features
        self.weight = nn.Parameter(weight_matrix.clone().detach().type(torch.float32),requires_grad=False)
        if bias:
            self.bias = nn.Parameter(torch.zeros(self.out_features,dtype=torch.float32), requires_grad=True)
        else:
            self.register_parameter('bias', None)

    def reset_parameters(self):
        torch.nn.init.kaiming_uniform_(self.weight, a=math.sqrt(5))
        if self.bias is not None:
            fan_in, _ = torch.nn.init._calculate_fan_in_and_fan_out(self.weight)
            bound = 1 / math.sqrt(fan_in) if fan_in > 0 else 0
            torch.nn.init.uniform_(self.bias, -bound, bound)

    def forward(self, input: torch.Tensor):
        return torch.nn.functional.linear(input, self.weight, self.bias)

    def extra_repr(self) -> str:
        return 'in_features={}, out_features={}, bias={}'.format(
            self.in_features, self.out_features, self.bias is not None
        )

class FCLayers(nn.Module):
    """
    A helper class to build fully-connected layers for a neural network. Adapted from scVI (https://github.com/scverse/scvi-tools)
    Parameters
    ----------
    n_in
        The dimensionality of the input
    n_out
        The dimensionality of the output
    n_layers
        The number of fully-connected hidden layers
    n_hidden
        The number of nodes per hidden layer
    dropout_rate
        Dropout rate to apply to each of the hidden layers
    use_batch_norm
        Whether to have `BatchNorm` layers or not
    use_activation
        Whether to have layer activation or not
    activation_fn
        Which activation function to use
    """

    def __init__(
        self,
        n_in: int,
        n_out: int,
        n_layers: int = 1,
        n_hidden: int = 128,
        dropout_rate: float = 0.1,
        use_batch_norm: bool = True,
        use_activation: bool = True,
        activation_fn: nn.Module = nn.ReLU,
    ):
        super().__init__()
        layers_dim = [n_in] + (n_layers - 1) * [n_hidden] + [n_out]

        self.fc_layers = nn.Sequential(
            collections.OrderedDict(
                [
                    (
                        f"Layer {i}",
                        nn.Sequential(
                            nn.Linear(
                                n_in ,
                                n_out,
                                bias=True,
                            ),
                            # non-default params come from defaults in original Tensorflow implementation
                            nn.BatchNorm1d(n_out, momentum=0.01, eps=0.001)
                            if use_batch_norm
                            else None,
                            activation_fn() if use_activation else None,
                            nn.Dropout(p=dropout_rate) if dropout_rate > 0 else None,
                        ),
                    )
                    for i, (n_in, n_out) in enumerate(
                        zip(layers_dim[:-1], layers_dim[1:])
                    )
                ]
            )
        )

    def forward(self, x: torch.Tensor):
        for i, layers in enumerate(self.fc_layers):
            for layer in layers:
                if layer is not None:
                        x = layer(x)
        return x


class FC_MeanScaleEncoder(nn.Module):


    def __init__(self, n_input: int, n_output: int, n_layers: int = 2, n_hidden: int = 128, dropout_rate: float = 0.1, use_batch_norm:bool=True,use_activation: bool = True,activation_fn: nn.Module = nn.ReLU):
        """Fully connected neural newtwork used to generate probability distribution over latent space used to encode observed data. 
        
        Parameters
        ----------
        n_input : int
            Dimension of the diagnostic space
        n_output : int
            Dimension of the latent space
        n_layers : int, optional
            Number of hidden layers in network. Default is 2.
        n_hidden : int, optional
            Number of hidden nodes. Default is 128.
        dropout_rate : float, optional
            Dropout rate for regularization during training. Default rate is 0.1. Set to 0.0 to remove dropout from training. 
        use_batch_norm : bool, optional
            Indicates whether to use batch normalization during traning. 
        use_activation : bool, optional
            Indicates whether to use activation function to transform final output of network. Default is True (improves expressivity via non-linearity)
        activation_fn : nn.Module, optional
            Activation function to use. Default is ReLU
        """
        super(FC_MeanScaleEncoder,self).__init__()

        self.encoder = FCLayers(n_in=n_input, n_out=n_hidden, n_layers=n_layers,
                                n_hidden=n_hidden, dropout_rate=dropout_rate,use_batch_norm=use_batch_norm,use_activation=use_activation,activation_fn=activation_fn)
        self.mean_encoder = nn.Linear(n_hidden, n_output,bias=True)
        self.var_encoder = nn.Linear(n_hidden, n_output,bias=True)

    def forward(self, x):
        r"""The forward computation for a single sample.
         #. Encodes the data into latent space using the encoder network
        :param x: tensor with shape (n_input,)
        :param cat_list: list of category membership(s) for this sample
        """

        # Parameters for latent distribution
        q = self.encoder(x)
        q_m = self.mean_encoder(q)
        log_q_v = self.var_encoder(q)+1e-6 #added to prevent underflow errors
        
        return q_m,torch.exp(0.5*log_q_v)




class FC_Decoder(nn.Module):

    def __init__(self, n_input: int, n_output: int, n_layers: int = 2, n_hidden: int = 128, dropout_rate: float = 0.1, use_batch_norm:bool=True,use_activation: bool = True,activation_fn: nn.Module = nn.ReLU):
        """Fully connected neural network used to decode latent phenotype space into logit-probabilities for a set of diagnoses.
        
        Parameters
        ----------
        n_input : int
            Dimension of the latent space
        n_output : int
            Dimension of the diagnostic space
        n_layers : int, optional
            Number of hidden layers in network. Default is 2.
        n_hidden : int, optional
            Number of hidden nodes. Default is 128.
        dropout_rate : float, optional
            Dropout rate for regularization during training. Default rate is 0.1. Set to 0.0 to remove dropout from training. 
        use_batch_norm : bool, optional
            Indicates whether to use batch normalization during traning. 
        use_activation : bool, optional
            Indicates whether to use activation function to transform final output of network. Default is True (improves expressivity via non-linearity)
        activation_fn : nn.Module, optional
            Activation function to use. Default is ReLU
        """
        super(FC_Decoder,self).__init__()
        self.nonlinear_latent = FCLayers(n_in=n_input, n_out=n_hidden, n_layers=n_layers,n_hidden=n_hidden,use_batch_norm=use_batch_norm,use_activation=use_activation,activation_fn=activation_fn)
        self.output_layer =  nn.Linear(n_hidden, n_output,bias=True)


    def forward(self,latent_var):
        return self.output_layer(self.nonlinear_latent(latent_var))


    def _set_bias(self,bias_vec):
        with torch.no_grad():
            self.output_layer.bias[:]=bias_vec[:]

class Linear_Decoder(nn.Module):


    
    def __init__(self,n_input: int, n_output: int):
        """Decodes a latent space into the paramters defining the logit-probabilities for a set of diagnoses.
        
        Parameters
        ----------
        n_input : int
            Dimension of the latent space
        n_output : int
            Dimension of the symptom space
        """
        super(Linear_Decoder,self).__init__()
        self.linear_latent = nn.Linear(n_input,n_output,bias=True)

    def forward(self,latent_var):
        return self.linear_latent(latent_var)

    def _set_bias(self,bias_vec):
        with torch.no_grad():
            self.linear_latent.bias[:]=bias_vec[:]



class Fixed_Linear_Decoder(nn.Module):
    def __init__(self, decoding_matrix):
        """Decodes a latent space into the paramters defining the logit-probabilities for a set of diagnoses. The dimension of the diagnosis space is determined from the decoding_matrix provided by the user (dim=1). Note, the decoding matrix is NOT updated during inference. 
        
        Parameters
        ----------
        decoding_matrix : np.array or torch.tensor

        Matrix used to decode a latent variable space (dim=0) into a set of logit parameters defining diagnostic probabilities. 
        
        """
        super(Fixed_Linear_Decoder,self).__init__()
        self.linear_latent=FixedWeights_Linear(decoding_matrix.shape[1],decoding_matrix.shape[0],decoding_matrix,bias=True)

    def _set_bias(self,bias_vec):
        with torch.no_grad():
            self.linear_latent.bias[:]=bias_vec[:]

    def forward(self,latent_var):
        return self.linear_latent(latent_var)








