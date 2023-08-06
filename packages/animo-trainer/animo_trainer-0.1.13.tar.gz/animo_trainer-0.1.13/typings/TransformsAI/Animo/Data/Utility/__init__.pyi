import typing, abc
from TransformsAI.Animo.Data.Models import CheckpointData, RewardOccurrenceData
from System.Collections.Generic import List_1
from TransformsAI.Animo.Learning.Rewards import NewReward

class AgentCheckpointAccumulator:
    def __init__(self) -> None: ...
    def AddReward(self, index: int, stepCount: int) -> None: ...
    def CreateCheckpoint(self, agentId: int, timestamp: int, trainingSessionId: str, rewards: List_1[NewReward], occurrences: List_1[RewardOccurrenceData], episodeLengths: List_1[int]) -> CheckpointData: ...
    def OnCheckpointCreated(self, checkpointTimestamp: int, agentId: int, sessionId: str, rewards: List_1[NewReward]) -> CheckpointData: ...
    def OnEpisodeEnded(self, stepCount: int) -> None: ...


class Serializer(abc.ABC):
    @staticmethod
    def ToJson(obj: typing.Any) -> str: ...
    # Skipped FromJson due to it being static, abstract and generic.

    FromJson : FromJson_MethodGroup
    class FromJson_MethodGroup:
        def __getitem__(self, t:typing.Type[FromJson_1_T1]) -> FromJson_1[FromJson_1_T1]: ...

        FromJson_1_T1 = typing.TypeVar('FromJson_1_T1')
        class FromJson_1(typing.Generic[FromJson_1_T1]):
            FromJson_1_T = Serializer.FromJson_MethodGroup.FromJson_1_T1
            def __call__(self, json: str) -> FromJson_1_T:...



