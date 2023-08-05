import CoreServices
from PyObjCTools.TestSupport import TestCase


class TestUnicodeUtilities(TestCase):
    def assert_not_wrapped(self, name):
        self.assertTrue(
            not hasattr(CoreServices, name), f"{name!r} exposed in bindings"
        )

    def test_not_wrapped(self):
        self.assert_not_wrapped("kUCKeyOutputStateIndexMask")
        self.assert_not_wrapped("kUCKeyOutputSequenceIndexMask")
        self.assert_not_wrapped("kUCKeyOutputTestForIndexMask")
        self.assert_not_wrapped("kUCKeyOutputGetIndexMask")
        self.assert_not_wrapped("UCKeyStateRecord")
        self.assert_not_wrapped("kUCKeyStateEntryTerminalFormat")
        self.assert_not_wrapped("kUCKeyStateEntryRangeFormat")
        self.assert_not_wrapped("UCKeyStateEntryTerminal")
        self.assert_not_wrapped("UCKeyStateEntryRange")
        self.assert_not_wrapped("UCKeyboardTypeHeader")
        self.assert_not_wrapped("UCKeyboardLayout")
        self.assert_not_wrapped("UCKeyLayoutFeatureInfo")
        self.assert_not_wrapped("UCKeyModifiersToTableNum")
        self.assert_not_wrapped("UCKeyToCharTableIndex")
        self.assert_not_wrapped("UCKeyStateRecordsIndex")
        self.assert_not_wrapped("UCKeyStateTerminators")
        self.assert_not_wrapped("UCKeySequenceDataIndex")
        self.assert_not_wrapped("kUCKeyLayoutHeaderFormat")
        self.assert_not_wrapped("kUCKeyLayoutFeatureInfoFormat")
        self.assert_not_wrapped("kUCKeyModifiersToTableNumFormat")
        self.assert_not_wrapped("kUCKeyToCharTableIndexFormat")
        self.assert_not_wrapped("kUCKeyStateRecordsIndexFormat")
        self.assert_not_wrapped("kUCKeyStateTerminatorsFormat")
        self.assert_not_wrapped("kUCKeySequenceDataIndexFormat")
        self.assert_not_wrapped("kUCKeyActionDown")
        self.assert_not_wrapped("kUCKeyActionUp")
        self.assert_not_wrapped("kUCKeyActionAutoKey")
        self.assert_not_wrapped("kUCKeyActionDisplay")
        self.assert_not_wrapped("kUCKeyTranslateNoDeadKeysBit")
        self.assert_not_wrapped("kUCKeyTranslateNoDeadKeysMask")
        self.assert_not_wrapped("kUnicodeCollationClass")
        self.assert_not_wrapped("CollatorRef")
        self.assert_not_wrapped("kUCCollateComposeInsensitiveMask")
        self.assert_not_wrapped("kUCCollateWidthInsensitiveMask")
        self.assert_not_wrapped("kUCCollateCaseInsensitiveMask")
        self.assert_not_wrapped("kUCCollateDiacritInsensitiveMask")
        self.assert_not_wrapped("kUCCollatePunctuationSignificantMask")
        self.assert_not_wrapped("kUCCollateDigitsOverrideMask")
        self.assert_not_wrapped("kUCCollateDigitsAsNumberMask")
        self.assert_not_wrapped("kUCCollateStandardOptions")
        self.assert_not_wrapped("kUCCollateTypeHFSExtended")
        self.assert_not_wrapped("kUCCollateTypeSourceMask")
        self.assert_not_wrapped("kUCCollateTypeShiftBits")
        self.assert_not_wrapped("kUCCollateTypeMask")
        self.assert_not_wrapped("kUCTSDirectionNext")
        self.assert_not_wrapped("kUCTSDirectionPrevious")
        self.assert_not_wrapped("kUCTSOptionsNoneMask")
        self.assert_not_wrapped("kUCTSOptionsReleaseStringMask")
        self.assert_not_wrapped("kUCTSOptionsDataIsOrderedMask")
        self.assert_not_wrapped("NewIndexToUCStringUPP")
        self.assert_not_wrapped("DisposeIndexToUCStringUPP")
        self.assert_not_wrapped("InvokeIndexToUCStringUPP")
        self.assert_not_wrapped("kUCTypeSelectMaxListSize")
        self.assert_not_wrapped("kUnicodeTextBreakClass")
        self.assert_not_wrapped("kUCTextBreakCharMask")
        self.assert_not_wrapped("kUCTextBreakClusterMask")
        self.assert_not_wrapped("kUCTextBreakWordMask")
        self.assert_not_wrapped("kUCTextBreakLineMask")
        self.assert_not_wrapped("kUCTextBreakParagraphMask")
        self.assert_not_wrapped("kUCTextBreakLeadingEdgeMask")
        self.assert_not_wrapped("kUCTextBreakGoBackwardsMask")
        self.assert_not_wrapped("kUCTextBreakIterateMask")
        self.assert_not_wrapped("UCKeyTranslate")
        self.assert_not_wrapped("UCCreateCollator")
        self.assert_not_wrapped("UCGetCollationKey")
        self.assert_not_wrapped("UCCompareCollationKeys")
        self.assert_not_wrapped("UCCompareText")
        self.assert_not_wrapped("UCDisposeCollator")
        self.assert_not_wrapped("UCCompareTextDefault")
        self.assert_not_wrapped("UCCompareTextNoLocale")
        self.assert_not_wrapped("UCCreateTextBreakLocator")
        self.assert_not_wrapped("UCFindTextBreak")
        self.assert_not_wrapped("UCDisposeTextBreakLocator")
        self.assert_not_wrapped("UCTypeSelectCreateSelector")
        self.assert_not_wrapped("UCTypeSelectFlushSelectorData")
        self.assert_not_wrapped("UCTypeSelectReleaseSelector")
        self.assert_not_wrapped("UCTypeSelectWouldResetBuffer")
        self.assert_not_wrapped("UCTypeSelectAddKeyToSelector")
        self.assert_not_wrapped("UCTypeSelectCompare")
        self.assert_not_wrapped("UCTypeSelectFindItem")
        self.assert_not_wrapped("UCTypeSelectWalkList")
