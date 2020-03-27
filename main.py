import argparse
from model_search import run_model_search_cnn, run_model_search_mlp

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("--network", type = str, default='cnn', help = "Choose from 'cnn' or 'mlp'")
parser.add_argument("--data_folder", type = str, default='./', help = "Path to folder where dataset is stored")
parser.add_argument("--dataset", type = str, default='cifar10', help = "For CNNs, choose from 'cifar10', 'cifar100', 'mnist', 'fmnist'. For MLPs, choose from 'mnist', 'fmnist', 'rcv1_2000'.")
parser.add_argument("--val_split", type = float, default = 1/5, help = "Fraction of complete training data to use for validation")
parser.add_argument("--augment", type = bool, default=True, help = "<CNNs only> Whether to apply basic augmentation")
parser.add_argument("--verbose", type = bool, default = False, help = "print messages after every epoch")

parser.add_argument("--wc", type = float, default = 0.1, help = "Complexity penalty coefficient")
parser.add_argument("--penalize", type = str, default = 't_epoch', help = "<MLPs only> Choose from 't_epoch' for training time per epoch, or 'numparams' for number of trainable parameters (CNNs only support t_epoch)")
parser.add_argument("--tbar_epoch", type = float, default = '10', help = "Baseline time to normalize t_epoch. Platform dependent.")
parser.add_argument("--numepochs", type = int, default = 100, help = "How many epochs to run each model for")
parser.add_argument("--val_patience", type = int, default = 1000000000, help = "Terminate training if val accuracy doesn't increase for this many epochs. The default is basically infinity.")

parser.add_argument("--bo_prior_states", type = int, default = 15, help = "# prior states for Bayesian optimization")
parser.add_argument("--bo_steps", type = int, default = 15, help = "# optimization steps for Bayesian optimization")
parser.add_argument("--bo_explore", type = int, default = 1000, help = "# states each step of acquisition function explores in Bayesian optimization")
parser.add_argument("--grid_search_order", type = str, nargs = 4, default = ['ds','bn','do','sc'], metavar = ('ds/bn/do/sc', 'ds/bn/do/sc', 'ds/bn/do/sc', 'ds/bn/do/sc'), help = "<CNNs only> Any permutation of downsampling 'ds', batch normalization 'bn', dropout 'do' and shortcut connections 'sc'")

parser.add_argument("--num_conv_layers", type = int, nargs = 2, default = [4,16], metavar = ('lower_limit', 'upper_limit'), help = "<CNNs only> Limits for # conv layers")
parser.add_argument("--channels_first", type = int, nargs = 2, default = [16,64], metavar = ('lower_limit', 'upper_limit'), help = "<CNNs only> Limits for # channels in 1st conv layer")
parser.add_argument("--channels_upper", type = int, default = 512, help = "<CNNs only> Upper limit for # channels in any conv layer")
parser.add_argument("--num_hidden_layers", type = int, nargs = 2, default = [0,2], metavar = ('lower_limit', 'upper_limit'), help = "<MLPs only> Limits for # hidden layers")
parser.add_argument("--hidden_nodes", type = int, nargs = 2, default = [20,400], metavar = ('lower_limit', 'upper_limit'), help = "<MLPs only> Limits for # hidden nodes")
parser.add_argument("--lr", type = float, nargs = 2, default = [-5,-1], metavar = ('lower_log_limit', 'upper_log_limit'), help = "Log limits for learning rate")
parser.add_argument("--weight_decay", type = float, nargs = 2, default = [-6,-3], metavar = ('lower_log_limit', 'upper_log_limit'), help = "Log limits for weight decay (lowest order of magnitude converted to 0 weight decay)")
parser.add_argument("--batch_size", type = int, nargs = 2, default = [32,512], metavar = ('lower_limit', 'upper_limit'), help = "Limits for batch size")

parser.add_argument("--bn_fracs", type = float, nargs = '+', default = [0,0.25,0.5,0.75,1], help = "<CNNs only> What fractions of batch norm layers to explore")
parser.add_argument("--do_fracs", type = float, nargs = '+', default = [0,0.25,0.5,0.75,1], help = "<CNNs only> What fractions of dropout layers to explore")
parser.add_argument("--input_drop_probs", type = float, nargs = '+', default = [0.1,0.2], help = "<CNNs only> What drop probabilities to explore in input layer")
parser.add_argument("--drop_probs_cnn", type = float, nargs = '+', default = [0.15,0.3,0.45], help = "<CNNs only> What drop probabilities to explore in non-input layers")
parser.add_argument("--drop_probs_mlp", type = float, nargs = '+', default = [0,0.1,0.2,0.3,0.4,0.5], help = "<MLPs only> What drop probabilities to explore in hidden layers")

parser.add_argument("--num_best", type = int, default = 1, help = "# best models to return from final stage of search")
parser.add_argument("--prior_time", type = float, default = 0.0, help = "When resuming a run, enter time elapsed so far (useful for getting accurate time estimate)")

args = parser.parse_args()


if args.network == 'cnn':
    run_model_search_cnn(data_folder=args.data_folder, dataset=args.dataset, val_split=args.val_split, augment=args.augment, verbose=args.verbose,
                         wc=args.wc, tbar_epoch=args.tbar_epoch, numepochs=args.numepochs, val_patience=args.val_patience,
                         bo_prior_states=args.bo_prior_states, bo_steps=args.bo_steps, bo_explore=args.bo_explore, grid_search_order=args.grid_search_order,
                         num_conv_layers=args.num_conv_layers, channels_first=args.channels_first, channels_upper=args.channels_upper, lr=args.lr, weight_decay=args.weight_decay, batch_size=args.batch_size,
                         bn_fracs=args.bn_fracs, do_fracs=args.do_fracs, input_drop_probs=args.input_drop_probs, drop_probs=args.drop_probs_cnn,
                         num_best=args.num_best, prior_time=args.prior_time)
elif args.network == 'mlp':
    run_model_search_mlp(data_folder=args.data_folder, dataset=args.dataset, val_split=args.val_split, verbose=args.verbose,
                         wc=args.wc, penalize=args.penalize, tbar_epoch=args.tbar_epoch, numepochs=args.numepochs, val_patience=args.val_patience,
                         bo_prior_states=args.bo_prior_states, bo_steps=args.bo_steps, bo_explore=args.bo_explore,
                         num_hidden_layers=args.num_hidden_layers, hidden_nodes=args.hidden_nodes, lr=args.lr, weight_decay=args.weight_decay, batch_size=args.batch_size,
                         drop_probs=args.drop_probs_mlp,
                         num_best=args.num_best, prior_time=args.prior_time)

