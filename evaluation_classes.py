from dataclasses import dataclass
from typing import List, TypeVar, Generic
from decimal import Decimal

T = TypeVar('T')


@dataclass
class TransactionEvaluationData:
    tx_duration_in_ms: int
    tx_gas_used: Decimal
    tx_effective_gas_price: Decimal
    tx_cost: Decimal


@dataclass
class TransactionEvaluationType:
    user_signer_address: str
    user_iteration: int
    user_tx_iteration: int
    gas_used: int
    effective_gas_price: int
    cost: int
    duration_in_ms: int


@dataclass
class TransactionMetrics:
    avg: int
    median: int
    min: int
    max: int
    sum: int


@dataclass
class BNTransactionMetrics:
    avg: Decimal
    median: Decimal
    min: Decimal
    max: Decimal
    sum: Decimal


@dataclass
class TransactionEvaluationMetrics:
    gas_used: TransactionMetrics
    effective_gas_price: TransactionMetrics
    cost: TransactionMetrics
    duration_in_ms: TransactionMetrics


@dataclass
class EvaluationLogJsonInputType(Generic[T]):
    contract_name: str
    network: str
    date: str  # Use ISO 8601 formatted string to represent dates
    duration_in_ms: int
    ether_unit: str  # Assuming EtherUnits is an enumeration of string values
    contract_parameters: T
    number_of_users: int
    metrics: TransactionEvaluationMetrics
    data: List[TransactionEvaluationType]
