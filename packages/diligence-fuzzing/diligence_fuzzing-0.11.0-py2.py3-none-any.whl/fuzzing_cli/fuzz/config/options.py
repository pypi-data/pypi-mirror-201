import base64
import math
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union

import click

from fuzzing_cli.fuzz.config.pytimer import str_to_sec


class FuzzingOptions:
    def __init__(
        self,
        ide: Optional[str] = None,
        quick_check: bool = False,
        build_directory: Optional[str] = None,
        sources_directory: Optional[str] = None,
        deployed_contract_address: Optional[str] = None,
        targets: Optional[List[str]] = None,
        map_to_original_source: bool = False,
        rpc_url: str = "http://localhost:7545",
        faas_url: str = "https://fuzzing.diligence.tools",
        number_of_cores: int = 2,
        campaign_name_prefix: str = "untitled",
        corpus_target: Optional[str] = None,
        additional_contracts_addresses: Optional[Union[List[str], str]] = None,
        dry_run: bool = False,
        key: Optional[str] = None,
        project: Optional[str] = None,
        truffle_executable_path: Optional[str] = None,
        incremental: bool = False,
        time_limit: Optional[str] = None,
        chain_id: Optional[Union[str, int]] = None,
        enable_cheat_codes: Optional[bool] = None,
        foundry_tests: bool = False,
        target_contracts: Optional[Dict[str, Set[str]]] = None,
        _validate_key: bool = True,
    ):
        self.ide: Optional[str] = ide and ide.lower()
        self.quick_check = quick_check
        self.corpus_target = corpus_target
        self.map_to_original_source = map_to_original_source
        self.dry_run = dry_run
        self.build_directory: Path = self.make_absolute_path(build_directory)
        self.sources_directory: Optional[Path] = self.make_absolute_path(
            sources_directory
        )
        self.deployed_contract_address = deployed_contract_address
        self.target: List[str] = targets
        self.rpc_url = rpc_url
        self.faas_url = faas_url
        self.number_of_cores = int(number_of_cores)
        self.campaign_name_prefix = campaign_name_prefix
        self.truffle_executable_path = truffle_executable_path
        self.project = project
        self.incremental = incremental
        self.time_limit = self._parse_time_limit(time_limit)
        self.chain_id: Optional[str] = self.parse_chain_id(chain_id)
        self.enable_cheat_codes = (
            bool(enable_cheat_codes) if enable_cheat_codes is not None else None
        )
        self.foundry_tests = foundry_tests
        self.target_contracts = target_contracts

        self.auth_endpoint = None
        self.refresh_token = None
        self.auth_client_id = None

        self.validate(key, _validate_key)

        if key:
            (
                self.auth_endpoint,
                self.auth_client_id,
                self.refresh_token,
            ) = self._decode_refresh_token(key)

        if type(additional_contracts_addresses) == str:
            self.additional_contracts_addresses: Optional[List[str]] = [
                a.strip() for a in additional_contracts_addresses.split(",")
            ]
        else:
            self.additional_contracts_addresses = additional_contracts_addresses

    @staticmethod
    def parse_chain_id(chain_id: Optional[Union[str, int]]) -> Optional[str]:
        if chain_id is None or (type(chain_id) == str and len(chain_id) == 0):
            return None
        if type(chain_id) == int:
            return hex(chain_id)
        return chain_id

    @staticmethod
    def _parse_time_limit(time_limit: Optional[str]) -> Optional[int]:
        if not time_limit:
            return None
        try:
            return math.floor(str_to_sec(time_limit))
        except Exception as e:
            raise click.exceptions.UsageError(
                "Error parsing `time_limit` config parameter. Make sure the string in the correct format "
                '(e.g. "5d 3h 50m 15s 20ms 6us" or "24hrs,30mins")'
            ) from e

    @staticmethod
    def make_absolute_path(path: Optional[str] = None) -> Optional[Path]:
        if not path:
            return None
        if Path(path).is_absolute():
            return Path(path)
        return Path.cwd().joinpath(path)

    @classmethod
    def parse_obj(cls, obj):
        return cls(**obj)

    @classmethod
    def from_config(
        cls,
        config: Dict[str, Any],
        ide: Optional[str] = None,
        deployed_contract_address: Optional[str] = None,
        targets: Optional[List[str]] = None,
        map_to_original_source: Optional[bool] = None,
        corpus_target: Optional[str] = None,
        additional_contracts_addresses: Optional[Union[List[str], str]] = None,
        dry_run: bool = False,
        key: Optional[str] = None,
        project: Optional[str] = None,
        truffle_executable_path: Optional[str] = None,
        quick_check: Optional[bool] = None,
        build_directory: Optional[str] = None,
        sources_directory: Optional[str] = None,
        enable_cheat_codes: Optional[bool] = None,
        foundry_tests: bool = False,
        target_contracts: Optional[Dict[str, Set[str]]] = None,
        _validate_key: bool = True,
    ) -> "FuzzingOptions":
        return cls.parse_obj(
            {
                k: v
                for k, v in (
                    {
                        "ide": ide or config.get("ide"),
                        "quick_check": config.get("quick_check", False)
                        if quick_check is None
                        else quick_check,
                        "build_directory": build_directory
                        or config.get("build_directory"),
                        "sources_directory": sources_directory
                        or config.get("sources_directory"),
                        "deployed_contract_address": deployed_contract_address
                        or config.get("deployed_contract_address"),
                        "targets": targets or config.get("targets"),
                        "map_to_original_source": config.get(
                            "map_to_original_source", False
                        )
                        if map_to_original_source is None
                        else map_to_original_source,
                        "rpc_url": config.get("rpc_url"),
                        "faas_url": config.get("faas_url"),
                        "number_of_cores": config.get("number_of_cores"),
                        "campaign_name_prefix": config.get("campaign_name_prefix"),
                        "corpus_target": corpus_target or config.get("corpus_target"),
                        "additional_contracts_addresses": additional_contracts_addresses
                        or config.get("additional_contracts_addresses"),
                        "dry_run": dry_run,
                        "key": key,
                        "project": project or config.get("project"),
                        "truffle_executable_path": truffle_executable_path,
                        "incremental": config.get("incremental"),
                        "suggested_seed_seqs": config.get("suggested_seed_seqs"),
                        "lesson_description": config.get("lesson_description"),
                        "time_limit": config.get("time_limit"),
                        "chain_id": config.get("fuzzer_options", {}).get("chain_id"),
                        "enable_cheat_codes": config.get("fuzzer_options", {}).get(
                            "enable_cheat_codes"
                        )
                        if enable_cheat_codes is None
                        else enable_cheat_codes,
                        "foundry_tests": foundry_tests,
                        "target_contracts": target_contracts,
                        "_validate_key": _validate_key,
                    }
                ).items()
                if v is not None
            }
        )

    @staticmethod
    def _decode_refresh_token(refresh_token: str) -> Tuple[str, str, str]:
        error_message = (
            "API Key is malformed. The format is `<auth_data>::<refresh_token>`"
        )
        # format is "<auth_data>::<refresh_token>"
        if refresh_token.count("::") != 1:
            raise click.exceptions.UsageError(error_message)
        data, rt = refresh_token.split("::")
        if not data or not rt:
            raise click.exceptions.UsageError(error_message)
        try:
            decoded_data = base64.b64decode(data).decode()
        except:
            raise click.exceptions.UsageError(error_message)
        if decoded_data.count("::") != 1:
            raise click.exceptions.UsageError(error_message)
        client_id, endpoint = decoded_data.split("::")
        if not client_id or not endpoint:
            raise click.exceptions.UsageError(error_message)
        return endpoint, client_id, rt

    def validate(self, key: Optional[str] = None, __validate_key: bool = True):
        if not self.build_directory:
            raise click.exceptions.UsageError(
                "Build directory not provided. You need to set the `build_directory` "
                "under the `fuzz` key of your .fuzz.yml config file."
            )
        if not self.sources_directory:
            click.secho(
                "Warning: Sources directory not specified. Using IDE defaults. For a proper seed state check "
                "please set the `sources_directory` under the `fuzz` key of your .fuzz.yml config file."
            )

        if not key and __validate_key is True:
            raise click.exceptions.UsageError(
                "API key was not provided. You need to provide an API key as the `--key` parameter "
                "of the `fuzz run` command or as `FUZZ_API_KEY` environment variable."
            )
        if not self.quick_check and not self.deployed_contract_address:
            raise click.exceptions.UsageError(
                "Deployed contract address not provided. You need to provide an address as the `--address` "
                "parameter of the fuzz run command.\nYou can also set the `deployed_contract_address`"
                "on the `fuzz` key of your .fuzz.yml config file."
            )
        if not self.target:
            raise click.exceptions.UsageError(
                "Target not provided. You need to provide a target as the last parameter of the fuzz run command."
                "\nYou can also set the `targets` on the `fuzz` key of your .fuzz.yml config file."
            )

        if self.incremental and not self.project:
            raise click.exceptions.UsageError(
                "`incremental` config parameter is set to true without specifying `project`. "
                "Please provide the `project` in your .fuzz.yml config file."
            )
        if self.incremental and self.corpus_target:
            raise click.exceptions.UsageError(
                "Both `incremental` and `corpus_target` are set. Please set only one option in your config file"
            )

        if self.chain_id and not self.chain_id.startswith("0x"):
            raise click.exceptions.UsageError(
                f"`chain_id` is not in hex format (0x..). Please provide correct hex value"
            )
