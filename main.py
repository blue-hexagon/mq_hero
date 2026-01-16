from src.app_store import Store
from src.broker.topic import DeviceCategory
from src.business.company import Company
from src.business.farm import Farm
from src.business.manager import EnterpriseManager
from src.data.device import Device
from src.hero.logger import Logger

COMPANIES = {
    'msp_test': {
        Company(
            full_name="msp_test",
            short_name="msp_test",
            api_version=1
        ).add_description("RingstedOne's Test Environment")
    },
    'msp_staging': {
        Company(
            full_name="msp_stage",
            short_name="msp_stage",
            api_version=1
        ).add_description("RingstedOne's Staging Environment")
    },
    'AgriTech': {
        Company(
            full_name="AgriTech Solutions",
            short_name="agtech",
            api_version=1
        )
        .add_description("AgriTechs IoT-Solution.")
        .add_farm(
            Farm(farm_id="123abc", city="Taastrup", name="Rørendegaard"))
        .add_farm(
            Farm(farm_id="1abc", city="Taastrup", name="Rørendegaard"))
    }
}
if __name__ == '__main__':
    Store()
    Logger()
    msp = EnterpriseManager(msp_name="RingstedIT")
    for company in COMPANIES:
        msp.add_company(new_company=COMPANIES[company])

    Company("AgritTech", "RVF").add_farms(

    )
    c_rvf = msp.get_company("RVF")
    tb = TopicBuilder()
    d1 = Device(device_id=..., category=DeviceCategory.DRONES)
    # d1.add_topic(TopicCategory.IMAGE,datasource=...)
