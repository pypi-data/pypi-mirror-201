import os, time
from typing import Dict, Tuple, List, cast

from mlagents.torch_utils import torch
from torch.nn.modules import Module

from mlagents.trainers.settings import TrainerSettings
from mlagents.trainers.model_saver.torch_model_saver import TorchModelSaver
from mlagents.trainers.model_saver.torch_model_saver import DEFAULT_CHECKPOINT_NAME

from animo_trainer.animo_training_session import AnimoTrainingSession
from TransformsAI.Animo.Data import Serializer


class AnimoTorchModelSaver(TorchModelSaver):
    def __init__(
        self,
        trainer_settings: TrainerSettings,
        model_path: str,
        session: AnimoTrainingSession,
        load: bool = False):

        super().__init__(trainer_settings, model_path, load)

        self.session = session

    def save_checkpoint(self, behavior_name: str, step: int) -> Tuple[str, List[str]]:
        with self.session.lock:
            modules = cast(Dict[str, Module], self.modules)  # type: ignore
            state_dict = {
                name: module.state_dict() for name, module in modules.items()
            }

            os.makedirs(self.model_path, exist_ok=True)

            timestamp = int(time.time_ns() / 1000)
            accumulator = self.session.checkpoint_accumulators[behavior_name]
            agent_data = self.session.agent_datas[behavior_name]

            checkpoint_path = os.path.join(self.model_path, str(timestamp))
            pytorch_ckpt_path = f"{checkpoint_path}.pt"
            export_ckpt_path = f"{checkpoint_path}.onnx"

            default_pytorch_ckpt_path = os.path.join(self.model_path, DEFAULT_CHECKPOINT_NAME)
            default_export_ckpt_path = os.path.join(self.model_path,
                                                    "model")  # File format not required by export function

            # Overwriting recent save files
            # Save `checkpoint.pt`, this is needed to resume training
            torch.save(state_dict, default_pytorch_ckpt_path)  # type: ignore
            self.export(default_export_ckpt_path, behavior_name)

            # Writing historical save files
            torch.save(state_dict, pytorch_ckpt_path)  # type: ignore
            self.export(checkpoint_path, behavior_name)

            # Writing AnimoData and AnimoCheckpoint
            new_checkpoint = accumulator.OnCheckpointCreated(timestamp, agent_data.Id, self.session.id,
                                                             agent_data.CurrentRewards)

            if new_checkpoint:
                agent_data.AddAndSelectCheckpoint(new_checkpoint)
                json_checkpoint = Serializer.ToJson(new_checkpoint)
                json_agent = Serializer.ToJson(agent_data)

                default_animo_agent_path = os.path.join(self.model_path, "AgentData.json")
                animo_ckpt_path = f"{checkpoint_path}.json"

                with open(default_animo_agent_path, 'w') as cp_file:
                    cp_file.write(json_agent)

                with open(animo_ckpt_path, 'w') as cp_file:
                    cp_file.write(json_checkpoint)

                print(f"Animo-Learn::Checkpoint::{self.session.id}::{checkpoint_path}")
                return export_ckpt_path, [pytorch_ckpt_path, animo_ckpt_path]
            else:
                print(f"Animo-Learn::Error::Accumulator did not return new checkpoint")
                return export_ckpt_path, [pytorch_ckpt_path]
