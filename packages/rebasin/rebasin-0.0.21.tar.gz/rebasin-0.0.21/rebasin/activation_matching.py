from __future__ import annotations

from typing import Any, Union, Callable

import torch
from torch import nn
from torchview import FunctionNode, ModuleNode, TensorNode, draw_graph

NODE_TYPES = Union[FunctionNode, ModuleNode, TensorNode]  # noqa


class ActivationMatching:
    """
    TODO
    """

    def __init__(
            self,
            model_a: nn.Module,
            model_b: nn.Module,
            batch: Any,
            device_b: torch.device | str | None = None,
            verbose: bool = False,
    ) -> None:
        self.model_a = model_a
        self.model_b = model_b
        self.batch = batch
        self.device_b = device_b
        self.verbose = verbose
        self.output_a: Any | None = None
        self.output_b: Any | None = None

    def rebasin(self) -> None:
        """
        TODO
        """
        modules_a, modules_b = self._get_modules()

        for module_a, module_b in zip(modules_a, modules_b):
            self._rebasin(module_a, module_b)

    def _get_modules(self) -> tuple[list[nn.Module], list[nn.Module]]:
        """
        Return the modules of the two models in the order that they are called.
        """
        modules_a: list[nn.Module] = self._get_modules_of_model(self.model_a)
        modules_b: list[nn.Module] = self._get_modules_of_model(self.model_b)

        assert len(modules_a) == len(modules_b), \
            "The models have different architectures."
        return modules_a, modules_b

    def _get_modules_of_model(self, model: nn.Module) -> list[nn.Module]:
        id_to_module = {id(m): m for m in model.modules()}
        modules: list[nn.Module] = []

        work_nodes = set(
            draw_graph(self.model_a, self.batch, depth=1e12).root_container
        )
        visited_nodes: set[NODE_TYPES] = set()

        while work_nodes:
            new_nodes: set[NODE_TYPES] = set()
            for node in work_nodes:
                if node in visited_nodes:
                    continue

                visited_nodes.add(node)
                if isinstance(node, ModuleNode):
                    modules.append(id_to_module[node.compute_unit_id])

                new_nodes.update(set(node.children))

            work_nodes = new_nodes - visited_nodes

        return modules

    def _rebasin(self, module_a: nn.Module, module_b: nn.Module) -> None:
        # 1. Attach hooks to the modules.
        # 2. Forward pass to record the outputs.
        # 3. Detach hooks.
        # 4. Get the weights and biases of module_b.
        # 5. Compute the new weights and biases.

        # Steps 1-3
        handle_a = module_a.register_forward_hook(self._get_hook("a"))
        handle_b = module_b.register_forward_hook(self._get_hook("b"))
        self.model_a(self.batch)
        self.model_b(self.batch)
        handle_a.remove()
        handle_b.remove()

    def _get_hook(self, model: str) -> Callable[[nn.Module, Any, Any], None]:
        def hook(module: nn.Module, inputs: Any, outputs: Any) -> None:
            if model == "a":
                self.output_a = outputs
            elif model == "b":
                self.output_b = outputs
            else:
                raise ValueError(f"Internal error: got {model=}")

        return hook


