import torch
from typing import Callable, Iterable, Tuple
from torch import nn
from torch.optim.lr_scheduler import LambdaLR
# from util.database import MySQL

class AdamW(torch.optim.Optimizer):
    """
    Implements Adam algorithm with weight decay fix as introduced in `Decoupled Weight Decay Regularization
    <https://arxiv.org/abs/1711.05101>`__.

    Parameters:
        params (:obj:`Iterable[nn.parameter.Parameter]`):
            Iterable of parameters to optimize or dictionaries defining parameter groups.
        lr (:obj:`float`, `optional`, defaults to 1e-3):
            The learning rate to use.
        betas (:obj:`Tuple[float,float]`, `optional`, defaults to (0.9, 0.999)):
            Adam's betas parameters (b1, b2).
        epsilon (:obj:`float`, `optional`, defaults to 1e-6):
            Adam's epsilon for numerical stability.
        weight_decay (:obj:`float`, `optional`, defaults to 0):
            Decoupled weight decay to apply.
    """

    def __init__(
        self,
        params: Iterable[nn.parameter.Parameter],
        lr: float = 2e-5,
        betas: Tuple[float, float] = (0.9, 0.999),
        epsilon: float = 1e-5,
        weight_decay: float = 0.01,
    ):
        if lr < 0.0:
            raise ValueError(f"Invalid learning rate: {lr} - should be >= 0.0")
        if not 0.0 <= betas[0] < 1.0:
            raise ValueError(f"Invalid beta parameter: {betas[0]} - should be in [0.0, 1.0[")
        if not 0.0 <= betas[1] < 1.0:
            raise ValueError(f"Invalid beta parameter: {betas[1]} - should be in [0.0, 1.0[")
        if not 0.0 <= epsilon:
            raise ValueError(f"Invalid epsilon value: {epsilon} - should be >= 0.0")
        defaults = dict(lr=lr, betas=betas, epsilon=epsilon, weight_decay=weight_decay)
        super().__init__(params, defaults)

    def parameters(self):
        for group in self.param_groups:
            for p in group["params"]:
                yield p
    
    @torch.no_grad()
    def step(self, closure: Callable = None):
        """
        Performs a single optimization step.

        Arguments:
            closure (:obj:`Callable`, `optional`): A closure that reevaluates the model and returns the loss.
        """
        loss = None
        if closure is not None:
            loss = closure()

        total_norm = torch.nn.utils.clip_grad_norm_(self.parameters(), 1)
        print("total_norm =", total_norm)
        if torch.isnan(total_norm):
            print("total_norm is nan, skipping...")
            return
        
        for group in self.param_groups:
            for p in group["params"]:
                if p.grad is None:
                    continue
                
                g = p.grad.data

                state = self.state[p]

                # State initialization
                if len(state) == 0:
                    state["step"] = 0
                    # Exponential moving average of gradient values
                    state["m_t"] = torch.zeros_like(p.data)
                    # Exponential moving average of squared gradient values
                    state["v_t"] = torch.zeros_like(p.data)

                m_t, v_t = state["m_t"], state["v_t"]
                
                beta_1, beta_2 = group["betas"]
                
                m_t = (beta_1 * m_t) + (1 - beta_1) * g
                v_t = (beta_2 * v_t) + (1 - beta_2) * g.square()
    
                update = m_t / (v_t.sqrt() + group["epsilon"])

                if len(p.shape) > 1:
                    update += group["weight_decay"] * p.data
                    
                p.data -= group["lr"] * update
                
                state["m_t"], state["v_t"] = m_t, v_t
                state["step"] += 1 

        return loss


def get_polynomial_decay_schedule_with_warmup(
    optimizer, num_training_steps, warmup_proportion=0.1, lr_end=None, power=1.0, last_epoch=-1
):
    """
    Create a schedule with a learning rate that decreases as a polynomial decay from the initial lr set in the
    optimizer to end lr defined by `lr_end`, after a warmup period during which it increases linearly from 0 to the
    initial lr set in the optimizer.

    Args:
        optimizer (:class:`~torch.optim.Optimizer`):
            The optimizer for which to schedule the learning rate.
        num_warmup_steps (:obj:`int`):
            The number of steps for the warmup phase.
        num_training_steps (:obj:`int`):
            The total number of training steps.
        lr_end (:obj:`float`, `optional`, defaults to 1e-7):
            The end LR.
        power (:obj:`float`, `optional`, defaults to 1.0):
            Power factor.
        last_epoch (:obj:`int`, `optional`, defaults to -1):
            The index of the last epoch when resuming training.

    Note: `power` defaults to 1.0 as in the fairseq implementation, which in turn is based on the original BERT
    implementation at
    https://github.com/google-research/bert/blob/f39e881b169b9d53bea03d2d341b31707a6c052b/optimization.py#L37

    Return:
        :obj:`torch.optim.lr_scheduler.LambdaLR` with the appropriate schedule.

    """
    num_warmup_steps = int(num_training_steps * warmup_proportion) 
    lr_init = optimizer.defaults["lr"]
    if lr_end is None:
        lr_end = lr_init / 50
            
    if not (lr_init > lr_end):
        raise ValueError(f"lr_end ({lr_end}) must be be smaller than initial lr ({lr_init})")

    def lr_lambda(current_step: int):
        if current_step < num_warmup_steps:
            return float(current_step) / float(max(1, num_warmup_steps))
        elif current_step > num_training_steps:
            return lr_end / lr_init  # as LambdaLR multiplies by lr_init
        else:
            lr_range = lr_init - lr_end
            decay_steps = num_training_steps - num_warmup_steps
            pct_remaining = 1 - (current_step - num_warmup_steps) / decay_steps
            decay = lr_range * pct_remaining ** power + lr_end
            return decay / lr_init  # as LambdaLR multiplies by lr_init

    return LambdaLR(optimizer, lr_lambda, last_epoch)
