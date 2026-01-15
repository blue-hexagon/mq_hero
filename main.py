from src.app_store import Store
from src.business.company import Company
from src.data.device import Device
from src.business.farm import Farm
from src.broker.topic import DeviceCategory

if __name__ == '__main__':
    Store()
    Company("Ringsted Venture Farming", "RVF").add_farms(
        Farm(farm_id="123abc", city="Taastrup", name="Rørendegaard"),
        Farm(farm_id="1abc", city="Taastrup", name="Rørendegaard")
    )
    c_rvf = Company.get_company("RVF").
    tb = TopicBuilder()
    d1 = Device(device_id=..., category=DeviceCategory.DRONES)
    # d1.add_topic(TopicCategory.IMAGE,datasource=...)
