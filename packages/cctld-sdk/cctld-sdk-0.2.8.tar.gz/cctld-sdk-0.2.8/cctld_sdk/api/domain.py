from cctld_sdk.common.types import CCTLDActions
from cctld_sdk.models import Domain


class DomainApiMixin:
    def domain_list(self, start_at: int = 0, count: int = 100):
        data = {"id": start_at, "count": count}
        return self.send_command(
            action=CCTLDActions.DOMAIN_LIST,
            data=data,
        )

    def domain_detail(self, domain_id: int):
        data = {"id": domain_id}
        return self.send_command(
            action=CCTLDActions.DOMAIN_DETAIL,
            data=data,
        )

    def domain_detail_by_domain_name(self, domain_name: str):
        data = {"dname": domain_name}
        return self.send_command(
            action=CCTLDActions.DOMAIN_DETAIL_BY_DOMAIN_NAME, data=data
        )

    def domain_add(self, domain_obj: Domain):
        data = domain_obj.__dict__
        return self.send_command(action=CCTLDActions.DOMAIN_ADD, data=data)

    def domain_edit(self, domain_id: int, attrs_dict: dict):
        """
        attrs_dict should be :
        {
            "sCustID":int[required],
            "sAdminID":int[required],
            "sTechID": int[required],
            "sBillID":int[required],
            "pnsID":int[optional],
            "snsID":int[optional],
            "tnsID":int[optional],
            "qnsID":int[optional],
            "sDesc":str[optional],
            "lWhois":int[optional]
        }
        note that include only required fields and fields you want to change in attrs_dict
        """
        # sourcery skip: dict-assign-update-to-union
        data = {"id": domain_id, **attrs_dict}
        return self.send_command(action=CCTLDActions.DOMAIN_EDIT, data=data)

    def domain_deleg_list(self, start_at: int = 0, count: int = 100):
        data = {"id": start_at, "count": count}
        return self.send_command(action=CCTLDActions.DOMAIN_DELEG_LIST, data=data)

    def domain_deleg(self, domain_id: int, year: int):
        data = {"id": domain_id, "year": year}
        return self.send_command(action=CCTLDActions.DOMAIN_DELEG, data=data)

    def domain_activation(self, domain_id: int, year: int):
        data = {"id": domain_id, "year": year}  # fix incorrect id
        return self.send_command(action=CCTLDActions.DOMAIN_ACTIVATION, data=data)

    def domain_status(self, domain_name: str):
        data = {"dname": domain_name}
        return self.send_command(action=CCTLDActions.DOMAIN_STATUS, data=data)

    def domain_delete(self, domain_id: int):
        data = {"id": domain_id}
        return self.send_command(action=CCTLDActions.DOMAIN_DELETE, data=data)

    def whois(self, domain_name: str):
        data = {"dname": domain_name}
        return self.send_command(action=CCTLDActions.WHOIS, data=data)
