from src.models.domain.activity import ActivityManager, BaseActivity, CompoundActivity
from src.models.domain.status import Attribute
from src.models.domain.profession import Profession
def test_perform_activity():
    attribute = Attribute("activeness", "spirit", True)
    attribute.load = 12
    base_activity_1=BaseActivity("create", 2.7, "create", [attribute])
    base_activity_2=BaseActivity("craft", 6.7, "others")
    profession_1 = Profession("Artist", "beginner")
    profession_1.load = 40
    compound_activity=CompoundActivity("sculpt", 40, [],[base_activity_1, base_activity_2],[profession_1])
    compound_activity2=CompoundActivity("chizzel", 30, [],[base_activity_1],[profession_1])
    
    activity_manager=ActivityManager()
    reward = activity_manager.perform_activity(compound_activity)
    reward2 = activity_manager.perform_activity_group([compound_activity, compound_activity2])
    assert reward == {'xp': 49.400000000000006, 'ap': {'activeness': 12}, 'pp': {'Artist': 40}}
    assert reward2 == {'xp': 82.10000000000001, 'ap': {'activeness': 24}, 'pp': {'Artist': 80}}
    