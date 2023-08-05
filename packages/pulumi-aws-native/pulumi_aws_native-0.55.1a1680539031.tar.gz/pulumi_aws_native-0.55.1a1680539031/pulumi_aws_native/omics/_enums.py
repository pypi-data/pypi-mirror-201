# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'AnnotationStoreEncryptionType',
    'AnnotationStoreStoreFormat',
    'AnnotationStoreStoreStatus',
    'ReferenceStoreEncryptionType',
    'SequenceStoreEncryptionType',
    'VariantStoreEncryptionType',
    'VariantStoreStoreStatus',
    'WorkflowEngine',
    'WorkflowStatus',
    'WorkflowType',
]


class AnnotationStoreEncryptionType(str, Enum):
    KMS = "KMS"


class AnnotationStoreStoreFormat(str, Enum):
    GFF = "GFF"
    TSV = "TSV"
    VCF = "VCF"


class AnnotationStoreStoreStatus(str, Enum):
    CREATING = "CREATING"
    UPDATING = "UPDATING"
    DELETING = "DELETING"
    ACTIVE = "ACTIVE"
    FAILED = "FAILED"


class ReferenceStoreEncryptionType(str, Enum):
    KMS = "KMS"


class SequenceStoreEncryptionType(str, Enum):
    KMS = "KMS"


class VariantStoreEncryptionType(str, Enum):
    KMS = "KMS"


class VariantStoreStoreStatus(str, Enum):
    CREATING = "CREATING"
    UPDATING = "UPDATING"
    DELETING = "DELETING"
    ACTIVE = "ACTIVE"
    FAILED = "FAILED"


class WorkflowEngine(str, Enum):
    WDL = "WDL"
    NEXTFLOW = "NEXTFLOW"


class WorkflowStatus(str, Enum):
    CREATING = "CREATING"
    ACTIVE = "ACTIVE"
    UPDATING = "UPDATING"
    DELETED = "DELETED"
    FAILED = "FAILED"


class WorkflowType(str, Enum):
    PRIVATE = "PRIVATE"
