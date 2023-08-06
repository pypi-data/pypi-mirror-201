from abinator import Abi, Struct, view, address

from abinator.common_abis import ERC20


class Factory(Abi):
    class Info(Struct):
        wallet: address
        defii: address
        hasAllocation: bool
        incentiveVault: address

    @view
    def getAllInfos() -> list[Info]:
        ...

    @view
    def getAllWallets() -> list[address]:
        ...


# print(Factory.functions)
# print(Factory.to_abi())


print(ERC20().transferFrom.selector)
