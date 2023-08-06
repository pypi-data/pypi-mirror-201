from typing import Dict, List, Optional

from langflow.custom.customs import get_custom_nodes
from langflow.interface.base import LangChainTypeCreator
from langflow.interface.custom_lists import chain_type_to_cls_dict
from langflow.settings import settings
from langflow.utils.util import build_template_from_class

# Assuming necessary imports for Field, Template, and FrontendNode classes


class ChainCreator(LangChainTypeCreator):
    type_name: str = "chains"

    @property
    def type_to_loader_dict(self) -> Dict:
        if self.type_dict is None:
            self.type_dict = chain_type_to_cls_dict
            from langflow.interface.chains.custom import CUSTOM_CHAINS

            self.type_dict.update(CUSTOM_CHAINS)
        return self.type_dict

    def get_signature(self, name: str) -> Optional[Dict]:
        try:
            if name in get_custom_nodes(self.type_name).keys():
                return get_custom_nodes(self.type_name)[name]
            return build_template_from_class(name, self.type_to_loader_dict)
        except ValueError as exc:
            raise ValueError("Chain not found") from exc

    def to_list(self) -> List[str]:
        custom_chains = list(get_custom_nodes("chains").keys())
        default_chains = list(self.type_to_loader_dict.keys())
        # Check if the chain is in the settings
        return [
            chain
            for chain in default_chains + custom_chains
            if chain in settings.chains or settings.dev
        ]


chain_creator = ChainCreator()
