# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'BotAliasStatus',
    'BotAudioRecognitionStrategy',
    'BotDialogActionType',
    'BotMessageSelectionStrategy',
    'BotObfuscationSettingObfuscationSettingType',
    'BotSlotConstraint',
    'BotSlotShape',
    'BotSlotValueResolutionStrategy',
    'BotVoiceSettingsEngine',
]


class BotAliasStatus(str, Enum):
    CREATING = "Creating"
    AVAILABLE = "Available"
    DELETING = "Deleting"
    FAILED = "Failed"


class BotAudioRecognitionStrategy(str, Enum):
    """
    Enables using slot values as a custom vocabulary when recognizing user utterances.
    """
    USE_SLOT_VALUES_AS_CUSTOM_VOCABULARY = "UseSlotValuesAsCustomVocabulary"


class BotDialogActionType(str, Enum):
    """
    The possible values of actions that the conversation can take.
    """
    CLOSE_INTENT = "CloseIntent"
    CONFIRM_INTENT = "ConfirmIntent"
    ELICIT_INTENT = "ElicitIntent"
    ELICIT_SLOT = "ElicitSlot"
    START_INTENT = "StartIntent"
    FULFILL_INTENT = "FulfillIntent"
    END_CONVERSATION = "EndConversation"
    EVALUATE_CONDITIONAL = "EvaluateConditional"
    INVOKE_DIALOG_CODE_HOOK = "InvokeDialogCodeHook"


class BotMessageSelectionStrategy(str, Enum):
    """
    Indicates how a message is selected from a message group among retries.
    """
    RANDOM = "Random"
    ORDERED = "Ordered"


class BotObfuscationSettingObfuscationSettingType(str, Enum):
    """
    Value that determines whether Amazon Lex obscures slot values in conversation logs. The default is to obscure the values.
    """
    NONE = "None"
    DEFAULT_OBFUSCATION = "DefaultObfuscation"


class BotSlotConstraint(str, Enum):
    REQUIRED = "Required"
    OPTIONAL = "Optional"


class BotSlotShape(str, Enum):
    """
    The different shapes that a slot can be in during a conversation.
    """
    SCALAR = "Scalar"
    LIST = "List"


class BotSlotValueResolutionStrategy(str, Enum):
    ORIGINAL_VALUE = "ORIGINAL_VALUE"
    TOP_RESOLUTION = "TOP_RESOLUTION"


class BotVoiceSettingsEngine(str, Enum):
    """
    Indicates the type of Amazon Polly voice that Amazon Lex should use for voice interaction with the user. For more information, see the engine parameter of the SynthesizeSpeech operation in the Amazon Polly developer guide.
    """
    STANDARD = "standard"
    NEURAL = "neural"
