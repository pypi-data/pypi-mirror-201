import torch
import torch.nn as nn
from typing import List
from deepchem.models.torch_models.grover_layers import GroverTransEncoder


class GroverPretrain(nn.Module):
    """The Grover Pretrain module.

    The GroverPretrain module is used for training an embedding based on the Grover Pretraining task.
    Grover pretraining is a self-supervised task where an embedding is trained to learn the contextual
    information of atoms and bonds along with graph-level properties, which are functional groups
    in case of molecular graphs.

    Parameters
    ----------
    embedding: nn.Module
        An embedding layer to generate embedding from input molecular graph
    atom_vocab_task_atom: nn.Module
        A layer used for predicting atom vocabulary from atom features generated via atom hidden states.
    atom_vocab_task_bond: nn.Module
        A layer used for predicting atom vocabulary from atom features generated via bond hidden states.
    bond_vocab_task_atom: nn.Module
        A layer used for predicting bond vocabulary from bond features generated via atom hidden states.
    bond_vocab_task_bond: nn.Module
        A layer used for predicting bond vocabulary from bond features generated via bond hidden states.

    Returns
    -------
    prediction_logits: Tuple
        A tuple of prediction logits containing prediction logits of atom vocabulary task from atom hidden state,
    prediction logits for atom vocabulary task from bond hidden states, prediction logits for bond vocabulary task
    from atom hidden states, prediction logits for bond vocabulary task from bond hidden states, functional
    group prediction logits from atom embedding generated from atom and bond hidden states, functional group
    prediction logits from bond embedding generated from atom and bond hidden states.

    Example
    -------
    >>> import deepchem as dc
    >>> from deepchem.feat.graph_data import BatchGraphData
    >>> from deepchem.utils.grover import extract_grover_attributes
    >>> from deepchem.models.torch_models.grover import GroverPretrain
    >>> from deepchem.models.torch_models.grover_layers import GroverEmbedding, GroverAtomVocabPredictor, GroverBondVocabPredictor, GroverFunctionalGroupPredictor
    >>> smiles = ['CC', 'CCC', 'CC(=O)C']

    >>> fg = dc.feat.CircularFingerprint()
    >>> featurizer = dc.feat.GroverFeaturizer(features_generator=fg)

    >>> graphs = featurizer.featurize(smiles)
    >>> batched_graph = BatchGraphData(graphs)
    >>> grover_graph_attributes = extract_grover_attributes(batched_graph)
    >>> f_atoms, f_bonds, a2b, b2a, b2revb, a2a, a_scope, b_scope, _, _ = grover_graph_attributes
    >>> components = {}
    >>> components['embedding'] = GroverEmbedding(node_fdim=f_atoms.shape[1], edge_fdim=f_bonds.shape[1])
    >>> components['atom_vocab_task_atom'] = GroverAtomVocabPredictor(vocab_size=10, in_features=128)
    >>> components['atom_vocab_task_bond'] = GroverAtomVocabPredictor(vocab_size=10, in_features=128)
    >>> components['bond_vocab_task_atom'] = GroverBondVocabPredictor(vocab_size=10, in_features=128)
    >>> components['bond_vocab_task_bond'] = GroverBondVocabPredictor(vocab_size=10, in_features=128)
    >>> components['functional_group_predictor'] = GroverFunctionalGroupPredictor(10)
    >>> model = GroverPretrain(**components)

    >>> inputs = f_atoms, f_bonds, a2b, b2a, b2revb, a_scope, b_scope, a2a
    >>> output = model(inputs)


    Reference
    ---------
    .. Rong, Yu, et al. "Self-supervised graph transformer on large-scale molecular data." Advances in Neural Information Processing Systems 33 (2020): 12559-12571.
    """

    def __init__(self, embedding: nn.Module, atom_vocab_task_atom: nn.Module,
                 atom_vocab_task_bond: nn.Module,
                 bond_vocab_task_atom: nn.Module,
                 bond_vocab_task_bond: nn.Module,
                 functional_group_predictor: nn.Module):
        super(GroverPretrain, self).__init__()
        self.embedding = embedding
        self.atom_vocab_task_atom = atom_vocab_task_atom
        self.atom_vocab_task_bond = atom_vocab_task_bond
        self.bond_vocab_task_atom = bond_vocab_task_atom
        self.bond_vocab_task_bond = bond_vocab_task_bond
        self.functional_group_predictor = functional_group_predictor

    def forward(self, graph_batch):
        """Forward function

        Parameters
        ----------
        graph_batch: List[torch.Tensor]
            A list containing grover graph attributes
        """
        _, _, _, _, _, atom_scope, bond_scope, _ = graph_batch
        atom_scope = atom_scope.data.cpu().numpy().tolist()
        bond_scope = bond_scope.data.cpu().numpy().tolist()

        embeddings = self.embedding(graph_batch)
        av_task_atom_pred = self.atom_vocab_task_atom(
            embeddings["atom_from_atom"])
        av_task_bond_pred = self.atom_vocab_task_bond(
            embeddings["atom_from_bond"])

        bv_task_atom_pred = self.bond_vocab_task_atom(
            embeddings["bond_from_atom"])
        bv_task_bond_pred = self.bond_vocab_task_bond(
            embeddings["bond_from_bond"])

        fg_prediction = self.functional_group_predictor(embeddings, atom_scope,
                                                        bond_scope)

        return av_task_atom_pred, av_task_bond_pred, bv_task_atom_pred, bv_task_bond_pred, fg_prediction[
            'atom_from_atom'], fg_prediction['atom_from_bond'], fg_prediction[
                'bond_from_atom'], fg_prediction['bond_from_bond']


class GroverEmbedding(nn.Module):
    """GroverEmbedding layer.

    This layer is a simple wrapper over GroverTransEncoder layer for retrieving the embeddings from the GroverTransEncoder corresponding to the `embedding_output_type` chosen by the user.

    Parameters
    ----------
    edge_fdim: int
        the dimension of additional feature for edge/bond.
    node_fdim: int
        the dimension of additional feature for node/atom.
    depth: int
        Dynamic message passing depth for use in MPNEncoder
    undirected: bool
        The message passing is undirected or not
    num_mt_block: int
        the number of message passing blocks.
    num_head: int
        the number of attention heads.
    """

    def __init__(self,
                 node_fdim,
                 edge_fdim,
                 embedding_output_type,
                 hidden_size=128,
                 depth=1,
                 undirected=False,
                 dropout=0.2,
                 activation='relu',
                 num_mt_block=1,
                 num_heads=4,
                 bias=False,
                 res_connection=False):
        super(GroverEmbedding, self).__init__()
        self.embedding_output_type = embedding_output_type
        self.encoders = GroverTransEncoder(
            hidden_size=hidden_size,
            edge_fdim=edge_fdim,
            node_fdim=node_fdim,
            depth=depth,
            undirected=undirected,
            dropout=dropout,
            activation=activation,
            num_mt_block=num_mt_block,
            num_heads=num_heads,
            embedding_output_type=embedding_output_type,
            bias=bias,
            res_connection=res_connection)

    def forward(self, graph_batch: List[torch.Tensor]):
        """Forward function

        Parameters
        ----------
        graph_batch: List[torch.Tensor]
            A list containing f_atoms, f_bonds, a2b, b2a, b2revb, a_scope, b_scope, a2a
        """
        output = self.encoders(graph_batch)
        if self.embedding_output_type == 'atom':
            return {
                "atom_from_atom": output[0],
                "atom_from_bond": output[1],
                "bond_from_atom": None,
                "bond_from_bond": None
            }  # atom_from_atom, atom_from_bond
        elif self.embedding_output_type == 'bond':
            return {
                "atom_from_atom": None,
                "atom_from_bond": None,
                "bond_from_atom": output[0],
                "bond_from_bond": output[1]
            }  # bond_from_atom, bond_from_bond
        elif self.embedding_output_type == "both":
            return {
                "atom_from_atom": output[0][0],
                "bond_from_atom": output[0][1],
                "atom_from_bond": output[1][0],
                "bond_from_bond": output[1][1]
            }
