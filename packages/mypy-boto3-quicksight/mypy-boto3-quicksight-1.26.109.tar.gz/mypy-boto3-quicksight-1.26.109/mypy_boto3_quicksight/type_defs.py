"""
Type annotations for quicksight service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_quicksight/type_defs/)

Usage::

    ```python
    from mypy_boto3_quicksight.type_defs import AccountCustomizationTypeDef

    data: AccountCustomizationTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, List, Mapping, Sequence, Union

from .literals import (
    AnalysisErrorTypeType,
    AnalysisFilterAttributeType,
    ArcThicknessOptionsType,
    ArcThicknessType,
    AssignmentStatusType,
    AuthenticationMethodOptionType,
    AxisBindingType,
    BarChartOrientationType,
    BarsArrangementType,
    BaseMapStyleTypeType,
    BoxPlotFillStyleType,
    CategoricalAggregationFunctionType,
    CategoryFilterMatchOperatorType,
    ColorFillTypeType,
    ColumnDataTypeType,
    ColumnRoleType,
    ColumnTagNameType,
    ComparisonMethodType,
    ConditionalFormattingIconSetTypeType,
    CrossDatasetTypesType,
    CustomContentImageScalingConfigurationType,
    CustomContentTypeType,
    DashboardBehaviorType,
    DashboardErrorTypeType,
    DashboardFilterAttributeType,
    DashboardUIStateType,
    DataLabelContentType,
    DataLabelOverlapType,
    DataLabelPositionType,
    DataSetFilterAttributeType,
    DataSetImportModeType,
    DataSourceErrorInfoTypeType,
    DataSourceFilterAttributeType,
    DataSourceTypeType,
    DateAggregationFunctionType,
    DayOfWeekType,
    EditionType,
    EmbeddingIdentityTypeType,
    FileFormatType,
    FilterNullOptionType,
    FilterOperatorType,
    FilterVisualScopeType,
    FolderFilterAttributeType,
    FontDecorationType,
    FontStyleType,
    FontWeightNameType,
    ForecastComputationSeasonalityType,
    FunnelChartMeasureDataLabelStyleType,
    GeoSpatialDataRoleType,
    GeospatialSelectedPointStyleType,
    HistogramBinTypeType,
    HorizontalTextAlignmentType,
    IconType,
    IdentityTypeType,
    IngestionErrorTypeType,
    IngestionRequestSourceType,
    IngestionRequestTypeType,
    IngestionStatusType,
    IngestionTypeType,
    InputColumnDataTypeType,
    JoinTypeType,
    LayoutElementTypeType,
    LegendPositionType,
    LineChartLineStyleType,
    LineChartMarkerShapeType,
    LineChartTypeType,
    LineInterpolationType,
    LookbackWindowSizeUnitType,
    MapZoomModeType,
    MaximumMinimumComputationTypeType,
    MemberTypeType,
    MissingDataTreatmentOptionType,
    NamespaceErrorTypeType,
    NamespaceStatusType,
    NegativeValueDisplayModeType,
    NumberScaleType,
    NumericEqualityMatchOperatorType,
    NumericSeparatorSymbolType,
    OtherCategoriesType,
    PanelBorderStyleType,
    PaperOrientationType,
    PaperSizeType,
    ParameterValueTypeType,
    PivotTableConditionalFormattingScopeRoleType,
    PivotTableMetricPlacementType,
    PivotTableSubtotalLevelType,
    PrimaryValueDisplayTypeType,
    RadarChartShapeType,
    ReferenceLineLabelHorizontalPositionType,
    ReferenceLineLabelVerticalPositionType,
    ReferenceLinePatternTypeType,
    ReferenceLineValueLabelRelativePositionType,
    RefreshIntervalType,
    RelativeDateTypeType,
    RelativeFontSizeType,
    ResizeOptionType,
    ResourceStatusType,
    RowLevelPermissionFormatVersionType,
    RowLevelPermissionPolicyType,
    SectionPageBreakStatusType,
    SelectedTooltipTypeType,
    SheetContentTypeType,
    SheetControlDateTimePickerTypeType,
    SheetControlListTypeType,
    SheetControlSliderTypeType,
    SimpleNumericalAggregationFunctionType,
    SortDirectionType,
    StatusType,
    TableBorderStyleType,
    TableCellImageScalingConfigurationType,
    TableOrientationType,
    TableTotalsPlacementType,
    TableTotalsScrollStatusType,
    TemplateErrorTypeType,
    TextQualifierType,
    TextWrapType,
    ThemeTypeType,
    TimeGranularityType,
    TooltipTitleTypeType,
    TopBottomComputationTypeType,
    TopBottomSortOrderType,
    URLTargetConfigurationType,
    UserRoleType,
    ValueWhenUnsetOptionType,
    VerticalTextAlignmentType,
    VisibilityType,
    VisualCustomActionTriggerType,
    WidgetStatusType,
    WordCloudCloudLayoutType,
    WordCloudWordCasingType,
    WordCloudWordOrientationType,
    WordCloudWordPaddingType,
    WordCloudWordScalingType,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "AccountCustomizationTypeDef",
    "AccountInfoTypeDef",
    "AccountSettingsTypeDef",
    "ActiveIAMPolicyAssignmentTypeDef",
    "AdHocFilteringOptionTypeDef",
    "ColumnIdentifierTypeDef",
    "AmazonElasticsearchParametersTypeDef",
    "AmazonOpenSearchParametersTypeDef",
    "CalculatedFieldTypeDef",
    "DataSetIdentifierDeclarationTypeDef",
    "EntityTypeDef",
    "AnalysisSearchFilterTypeDef",
    "DataSetReferenceTypeDef",
    "AnalysisSummaryTypeDef",
    "SheetTypeDef",
    "AnchorDateConfigurationTypeDef",
    "AnonymousUserDashboardEmbeddingConfigurationTypeDef",
    "DashboardVisualIdTypeDef",
    "AnonymousUserQSearchBarEmbeddingConfigurationTypeDef",
    "ArcAxisDisplayRangeTypeDef",
    "ArcConfigurationTypeDef",
    "ArcOptionsTypeDef",
    "AthenaParametersTypeDef",
    "AuroraParametersTypeDef",
    "AuroraPostgreSqlParametersTypeDef",
    "AwsIotAnalyticsParametersTypeDef",
    "DateAxisOptionsTypeDef",
    "AxisDisplayMinMaxRangeTypeDef",
    "AxisLinearScaleTypeDef",
    "AxisLogarithmicScaleTypeDef",
    "ItemsLimitConfigurationTypeDef",
    "BinCountOptionsTypeDef",
    "BinWidthOptionsTypeDef",
    "BorderStyleTypeDef",
    "BoxPlotStyleOptionsTypeDef",
    "PaginationConfigurationTypeDef",
    "CalculatedColumnTypeDef",
    "CalculatedMeasureFieldTypeDef",
    "CancelIngestionRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "CastColumnTypeOperationTypeDef",
    "CustomFilterConfigurationTypeDef",
    "CustomFilterListConfigurationTypeDef",
    "FilterListConfigurationTypeDef",
    "SimpleClusterMarkerTypeDef",
    "DataColorTypeDef",
    "ColumnDescriptionTypeDef",
    "ColumnGroupColumnSchemaTypeDef",
    "GeoSpatialColumnGroupTypeDef",
    "ColumnLevelPermissionRuleTypeDef",
    "ColumnSchemaTypeDef",
    "ConditionalFormattingSolidColorTypeDef",
    "ConditionalFormattingCustomIconOptionsTypeDef",
    "ConditionalFormattingIconDisplayConfigurationTypeDef",
    "ConditionalFormattingIconSetTypeDef",
    "TagTypeDef",
    "CreateAccountSubscriptionRequestRequestTypeDef",
    "SignupResponseTypeDef",
    "ResourcePermissionTypeDef",
    "DataSetUsageConfigurationTypeDef",
    "FieldFolderTypeDef",
    "RowLevelPermissionDataSetTypeDef",
    "SslPropertiesTypeDef",
    "VpcConnectionPropertiesTypeDef",
    "CreateFolderMembershipRequestRequestTypeDef",
    "FolderMemberTypeDef",
    "CreateGroupMembershipRequestRequestTypeDef",
    "GroupMemberTypeDef",
    "CreateGroupRequestRequestTypeDef",
    "GroupTypeDef",
    "CreateIAMPolicyAssignmentRequestRequestTypeDef",
    "CreateIngestionRequestRequestTypeDef",
    "CreateTemplateAliasRequestRequestTypeDef",
    "TemplateAliasTypeDef",
    "CreateThemeAliasRequestRequestTypeDef",
    "ThemeAliasTypeDef",
    "DecimalPlacesConfigurationTypeDef",
    "NegativeValueConfigurationTypeDef",
    "NullValueFormatConfigurationTypeDef",
    "FilterOperationSelectedFieldsConfigurationTypeDef",
    "LocalNavigationConfigurationTypeDef",
    "CustomActionURLOperationTypeDef",
    "CustomContentConfigurationTypeDef",
    "CustomNarrativeOptionsTypeDef",
    "CustomParameterValuesTypeDef",
    "InputColumnTypeDef",
    "DataPointDrillUpDownOptionTypeDef",
    "DataPointMenuLabelOptionTypeDef",
    "DataPointTooltipOptionTypeDef",
    "ExportToCSVOptionTypeDef",
    "ExportWithHiddenFieldsOptionTypeDef",
    "SheetControlsOptionTypeDef",
    "SheetLayoutElementMaximizationOptionTypeDef",
    "VisualAxisSortOptionTypeDef",
    "VisualMenuOptionTypeDef",
    "DashboardSearchFilterTypeDef",
    "DashboardSummaryTypeDef",
    "DashboardVersionSummaryTypeDef",
    "ExportHiddenFieldsOptionTypeDef",
    "DataBarsOptionsTypeDef",
    "DataColorPaletteTypeDef",
    "DataPathLabelTypeTypeDef",
    "FieldLabelTypeTypeDef",
    "MaximumLabelTypeTypeDef",
    "MinimumLabelTypeTypeDef",
    "RangeEndsLabelTypeTypeDef",
    "DataPathValueTypeDef",
    "DataSetSearchFilterTypeDef",
    "OutputColumnTypeDef",
    "DataSourceErrorInfoTypeDef",
    "DatabricksParametersTypeDef",
    "ExasolParametersTypeDef",
    "JiraParametersTypeDef",
    "MariaDbParametersTypeDef",
    "MySqlParametersTypeDef",
    "OracleParametersTypeDef",
    "PostgreSqlParametersTypeDef",
    "PrestoParametersTypeDef",
    "RdsParametersTypeDef",
    "RedshiftParametersTypeDef",
    "ServiceNowParametersTypeDef",
    "SnowflakeParametersTypeDef",
    "SparkParametersTypeDef",
    "SqlServerParametersTypeDef",
    "TeradataParametersTypeDef",
    "TwitterParametersTypeDef",
    "DataSourceSearchFilterTypeDef",
    "DataSourceSummaryTypeDef",
    "RollingDateConfigurationTypeDef",
    "DateTimeValueWhenUnsetConfigurationTypeDef",
    "DateTimeParameterTypeDef",
    "DecimalValueWhenUnsetConfigurationTypeDef",
    "DecimalParameterTypeDef",
    "DeleteAccountCustomizationRequestRequestTypeDef",
    "DeleteAccountSubscriptionRequestRequestTypeDef",
    "DeleteAnalysisRequestRequestTypeDef",
    "DeleteDashboardRequestRequestTypeDef",
    "DeleteDataSetRefreshPropertiesRequestRequestTypeDef",
    "DeleteDataSetRequestRequestTypeDef",
    "DeleteDataSourceRequestRequestTypeDef",
    "DeleteFolderMembershipRequestRequestTypeDef",
    "DeleteFolderRequestRequestTypeDef",
    "DeleteGroupMembershipRequestRequestTypeDef",
    "DeleteGroupRequestRequestTypeDef",
    "DeleteIAMPolicyAssignmentRequestRequestTypeDef",
    "DeleteNamespaceRequestRequestTypeDef",
    "DeleteRefreshScheduleRequestRequestTypeDef",
    "DeleteTemplateAliasRequestRequestTypeDef",
    "DeleteTemplateRequestRequestTypeDef",
    "DeleteThemeAliasRequestRequestTypeDef",
    "DeleteThemeRequestRequestTypeDef",
    "DeleteUserByPrincipalIdRequestRequestTypeDef",
    "DeleteUserRequestRequestTypeDef",
    "DescribeAccountCustomizationRequestRequestTypeDef",
    "DescribeAccountSettingsRequestRequestTypeDef",
    "DescribeAccountSubscriptionRequestRequestTypeDef",
    "DescribeAnalysisDefinitionRequestRequestTypeDef",
    "DescribeAnalysisPermissionsRequestRequestTypeDef",
    "DescribeAnalysisRequestRequestTypeDef",
    "DescribeDashboardDefinitionRequestRequestTypeDef",
    "DescribeDashboardPermissionsRequestRequestTypeDef",
    "DescribeDashboardRequestRequestTypeDef",
    "DescribeDataSetPermissionsRequestRequestTypeDef",
    "DescribeDataSetRefreshPropertiesRequestRequestTypeDef",
    "DescribeDataSetRequestRequestTypeDef",
    "DescribeDataSourcePermissionsRequestRequestTypeDef",
    "DescribeDataSourceRequestRequestTypeDef",
    "DescribeFolderPermissionsRequestRequestTypeDef",
    "DescribeFolderRequestRequestTypeDef",
    "DescribeFolderResolvedPermissionsRequestRequestTypeDef",
    "FolderTypeDef",
    "DescribeGroupMembershipRequestRequestTypeDef",
    "DescribeGroupRequestRequestTypeDef",
    "DescribeIAMPolicyAssignmentRequestRequestTypeDef",
    "IAMPolicyAssignmentTypeDef",
    "DescribeIngestionRequestRequestTypeDef",
    "DescribeIpRestrictionRequestRequestTypeDef",
    "DescribeNamespaceRequestRequestTypeDef",
    "DescribeRefreshScheduleRequestRequestTypeDef",
    "DescribeTemplateAliasRequestRequestTypeDef",
    "DescribeTemplateDefinitionRequestRequestTypeDef",
    "DescribeTemplatePermissionsRequestRequestTypeDef",
    "DescribeTemplateRequestRequestTypeDef",
    "DescribeThemeAliasRequestRequestTypeDef",
    "DescribeThemePermissionsRequestRequestTypeDef",
    "DescribeThemeRequestRequestTypeDef",
    "DescribeUserRequestRequestTypeDef",
    "UserTypeDef",
    "DonutCenterOptionsTypeDef",
    "ListControlSelectAllOptionsTypeDef",
    "ErrorInfoTypeDef",
    "ExcludePeriodConfigurationTypeDef",
    "FieldSortTypeDef",
    "FieldTooltipItemTypeDef",
    "GeospatialMapStyleOptionsTypeDef",
    "FilterSelectableValuesTypeDef",
    "SameSheetTargetVisualConfigurationTypeDef",
    "FilterOperationTypeDef",
    "FolderSearchFilterTypeDef",
    "FolderSummaryTypeDef",
    "FontSizeTypeDef",
    "FontWeightTypeDef",
    "FontTypeDef",
    "TimeBasedForecastPropertiesTypeDef",
    "WhatIfPointScenarioTypeDef",
    "WhatIfRangeScenarioTypeDef",
    "FreeFormLayoutScreenCanvasSizeOptionsTypeDef",
    "FreeFormLayoutElementBackgroundStyleTypeDef",
    "FreeFormLayoutElementBorderStyleTypeDef",
    "LoadingAnimationTypeDef",
    "SessionTagTypeDef",
    "GeospatialCoordinateBoundsTypeDef",
    "GetDashboardEmbedUrlRequestRequestTypeDef",
    "GetSessionEmbedUrlRequestRequestTypeDef",
    "TableBorderOptionsTypeDef",
    "GradientStopTypeDef",
    "GridLayoutScreenCanvasSizeOptionsTypeDef",
    "GridLayoutElementTypeDef",
    "GroupSearchFilterTypeDef",
    "GutterStyleTypeDef",
    "IAMPolicyAssignmentSummaryTypeDef",
    "LookbackWindowTypeDef",
    "QueueInfoTypeDef",
    "RowInfoTypeDef",
    "IntegerValueWhenUnsetConfigurationTypeDef",
    "IntegerParameterTypeDef",
    "JoinKeyPropertiesTypeDef",
    "ProgressBarOptionsTypeDef",
    "SecondaryValueOptionsTypeDef",
    "TrendArrowOptionsTypeDef",
    "LineChartLineStyleSettingsTypeDef",
    "LineChartMarkerStyleSettingsTypeDef",
    "MissingDataConfigurationTypeDef",
    "PaginatorConfigTypeDef",
    "ListAnalysesRequestRequestTypeDef",
    "ListControlSearchOptionsTypeDef",
    "ListDashboardVersionsRequestRequestTypeDef",
    "ListDashboardsRequestRequestTypeDef",
    "ListDataSetsRequestRequestTypeDef",
    "ListDataSourcesRequestRequestTypeDef",
    "ListFolderMembersRequestRequestTypeDef",
    "MemberIdArnPairTypeDef",
    "ListFoldersRequestRequestTypeDef",
    "ListGroupMembershipsRequestRequestTypeDef",
    "ListGroupsRequestRequestTypeDef",
    "ListIAMPolicyAssignmentsForUserRequestRequestTypeDef",
    "ListIAMPolicyAssignmentsRequestRequestTypeDef",
    "ListIngestionsRequestRequestTypeDef",
    "ListNamespacesRequestRequestTypeDef",
    "ListRefreshSchedulesRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTemplateAliasesRequestRequestTypeDef",
    "ListTemplateVersionsRequestRequestTypeDef",
    "TemplateVersionSummaryTypeDef",
    "ListTemplatesRequestRequestTypeDef",
    "TemplateSummaryTypeDef",
    "ListThemeAliasesRequestRequestTypeDef",
    "ListThemeVersionsRequestRequestTypeDef",
    "ThemeVersionSummaryTypeDef",
    "ListThemesRequestRequestTypeDef",
    "ThemeSummaryTypeDef",
    "ListUserGroupsRequestRequestTypeDef",
    "ListUsersRequestRequestTypeDef",
    "LongFormatTextTypeDef",
    "ManifestFileLocationTypeDef",
    "MarginStyleTypeDef",
    "NamespaceErrorTypeDef",
    "NumericRangeFilterValueTypeDef",
    "ThousandSeparatorOptionsTypeDef",
    "PercentileAggregationTypeDef",
    "StringParameterTypeDef",
    "PercentVisibleRangeTypeDef",
    "PivotTableConditionalFormattingScopeTypeDef",
    "PivotTablePaginatedReportOptionsTypeDef",
    "PivotTableFieldOptionTypeDef",
    "PivotTableFieldSubtotalOptionsTypeDef",
    "RowAlternateColorOptionsTypeDef",
    "ProjectOperationTypeDef",
    "RadarChartAreaStyleSettingsTypeDef",
    "ReferenceLineCustomLabelConfigurationTypeDef",
    "ReferenceLineStaticDataConfigurationTypeDef",
    "ReferenceLineStyleConfigurationTypeDef",
    "ScheduleRefreshOnEntityTypeDef",
    "RegisterUserRequestRequestTypeDef",
    "StatePersistenceConfigurationsTypeDef",
    "RegisteredUserQSearchBarEmbeddingConfigurationTypeDef",
    "RenameColumnOperationTypeDef",
    "RestoreAnalysisRequestRequestTypeDef",
    "RowLevelPermissionTagRuleTypeDef",
    "UploadSettingsTypeDef",
    "SectionAfterPageBreakTypeDef",
    "SpacingTypeDef",
    "SheetVisualScopingConfigurationTypeDef",
    "SheetTextBoxTypeDef",
    "SheetElementConfigurationOverridesTypeDef",
    "ShortFormatTextTypeDef",
    "StringValueWhenUnsetConfigurationTypeDef",
    "TableCellImageSizingConfigurationTypeDef",
    "TablePaginatedReportOptionsTypeDef",
    "TableFieldCustomIconContentTypeDef",
    "TemplateSourceTemplateTypeDef",
    "TextControlPlaceholderOptionsTypeDef",
    "UIColorPaletteTypeDef",
    "ThemeErrorTypeDef",
    "UntagColumnOperationTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateAccountSettingsRequestRequestTypeDef",
    "UpdateDashboardPublishedVersionRequestRequestTypeDef",
    "UpdateFolderRequestRequestTypeDef",
    "UpdateGroupRequestRequestTypeDef",
    "UpdateIAMPolicyAssignmentRequestRequestTypeDef",
    "UpdateIpRestrictionRequestRequestTypeDef",
    "UpdatePublicSharingSettingsRequestRequestTypeDef",
    "UpdateTemplateAliasRequestRequestTypeDef",
    "UpdateThemeAliasRequestRequestTypeDef",
    "UpdateUserRequestRequestTypeDef",
    "WaterfallChartOptionsTypeDef",
    "WordCloudOptionsTypeDef",
    "UpdateAccountCustomizationRequestRequestTypeDef",
    "AxisLabelReferenceOptionsTypeDef",
    "CascadingControlSourceTypeDef",
    "CategoryDrillDownFilterTypeDef",
    "ContributionAnalysisDefaultTypeDef",
    "DynamicDefaultValueTypeDef",
    "NumericEqualityDrillDownFilterTypeDef",
    "ParameterSelectableValuesTypeDef",
    "TimeEqualityFilterTypeDef",
    "TimeRangeDrillDownFilterTypeDef",
    "AnalysisErrorTypeDef",
    "DashboardErrorTypeDef",
    "TemplateErrorTypeDef",
    "SearchAnalysesRequestRequestTypeDef",
    "AnalysisSourceTemplateTypeDef",
    "DashboardSourceTemplateTypeDef",
    "TemplateSourceAnalysisTypeDef",
    "AnonymousUserDashboardVisualEmbeddingConfigurationTypeDef",
    "RegisteredUserDashboardVisualEmbeddingConfigurationTypeDef",
    "ArcAxisConfigurationTypeDef",
    "AxisDisplayRangeTypeDef",
    "AxisScaleTypeDef",
    "HistogramBinOptionsTypeDef",
    "TileStyleTypeDef",
    "BoxPlotOptionsTypeDef",
    "CreateColumnsOperationTypeDef",
    "CancelIngestionResponseTypeDef",
    "CreateAccountCustomizationResponseTypeDef",
    "CreateAnalysisResponseTypeDef",
    "CreateDashboardResponseTypeDef",
    "CreateDataSetResponseTypeDef",
    "CreateDataSourceResponseTypeDef",
    "CreateFolderResponseTypeDef",
    "CreateIAMPolicyAssignmentResponseTypeDef",
    "CreateIngestionResponseTypeDef",
    "CreateNamespaceResponseTypeDef",
    "CreateRefreshScheduleResponseTypeDef",
    "CreateTemplateResponseTypeDef",
    "CreateThemeResponseTypeDef",
    "DeleteAccountCustomizationResponseTypeDef",
    "DeleteAccountSubscriptionResponseTypeDef",
    "DeleteAnalysisResponseTypeDef",
    "DeleteDashboardResponseTypeDef",
    "DeleteDataSetRefreshPropertiesResponseTypeDef",
    "DeleteDataSetResponseTypeDef",
    "DeleteDataSourceResponseTypeDef",
    "DeleteFolderMembershipResponseTypeDef",
    "DeleteFolderResponseTypeDef",
    "DeleteGroupMembershipResponseTypeDef",
    "DeleteGroupResponseTypeDef",
    "DeleteIAMPolicyAssignmentResponseTypeDef",
    "DeleteNamespaceResponseTypeDef",
    "DeleteRefreshScheduleResponseTypeDef",
    "DeleteTemplateAliasResponseTypeDef",
    "DeleteTemplateResponseTypeDef",
    "DeleteThemeAliasResponseTypeDef",
    "DeleteThemeResponseTypeDef",
    "DeleteUserByPrincipalIdResponseTypeDef",
    "DeleteUserResponseTypeDef",
    "DescribeAccountCustomizationResponseTypeDef",
    "DescribeAccountSettingsResponseTypeDef",
    "DescribeAccountSubscriptionResponseTypeDef",
    "DescribeIpRestrictionResponseTypeDef",
    "GenerateEmbedUrlForAnonymousUserResponseTypeDef",
    "GenerateEmbedUrlForRegisteredUserResponseTypeDef",
    "GetDashboardEmbedUrlResponseTypeDef",
    "GetSessionEmbedUrlResponseTypeDef",
    "ListAnalysesResponseTypeDef",
    "ListIAMPolicyAssignmentsForUserResponseTypeDef",
    "PutDataSetRefreshPropertiesResponseTypeDef",
    "RestoreAnalysisResponseTypeDef",
    "SearchAnalysesResponseTypeDef",
    "TagResourceResponseTypeDef",
    "UntagResourceResponseTypeDef",
    "UpdateAccountCustomizationResponseTypeDef",
    "UpdateAccountSettingsResponseTypeDef",
    "UpdateAnalysisResponseTypeDef",
    "UpdateDashboardPublishedVersionResponseTypeDef",
    "UpdateDashboardResponseTypeDef",
    "UpdateDataSetPermissionsResponseTypeDef",
    "UpdateDataSetResponseTypeDef",
    "UpdateDataSourcePermissionsResponseTypeDef",
    "UpdateDataSourceResponseTypeDef",
    "UpdateFolderResponseTypeDef",
    "UpdateIAMPolicyAssignmentResponseTypeDef",
    "UpdateIpRestrictionResponseTypeDef",
    "UpdatePublicSharingSettingsResponseTypeDef",
    "UpdateRefreshScheduleResponseTypeDef",
    "UpdateTemplateResponseTypeDef",
    "UpdateThemeResponseTypeDef",
    "CategoryFilterConfigurationTypeDef",
    "ClusterMarkerTypeDef",
    "ColorScaleTypeDef",
    "ColumnTagTypeDef",
    "ColumnGroupSchemaTypeDef",
    "ColumnGroupTypeDef",
    "DataSetSchemaTypeDef",
    "ConditionalFormattingCustomIconConditionTypeDef",
    "CreateAccountCustomizationRequestRequestTypeDef",
    "CreateNamespaceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "CreateAccountSubscriptionResponseTypeDef",
    "CreateFolderRequestRequestTypeDef",
    "DescribeAnalysisPermissionsResponseTypeDef",
    "DescribeDataSetPermissionsResponseTypeDef",
    "DescribeDataSourcePermissionsResponseTypeDef",
    "DescribeFolderPermissionsResponseTypeDef",
    "DescribeFolderResolvedPermissionsResponseTypeDef",
    "DescribeTemplatePermissionsResponseTypeDef",
    "DescribeThemePermissionsResponseTypeDef",
    "LinkSharingConfigurationTypeDef",
    "UpdateAnalysisPermissionsRequestRequestTypeDef",
    "UpdateAnalysisPermissionsResponseTypeDef",
    "UpdateDashboardPermissionsRequestRequestTypeDef",
    "UpdateDataSetPermissionsRequestRequestTypeDef",
    "UpdateDataSourcePermissionsRequestRequestTypeDef",
    "UpdateFolderPermissionsRequestRequestTypeDef",
    "UpdateFolderPermissionsResponseTypeDef",
    "UpdateTemplatePermissionsRequestRequestTypeDef",
    "UpdateTemplatePermissionsResponseTypeDef",
    "UpdateThemePermissionsRequestRequestTypeDef",
    "UpdateThemePermissionsResponseTypeDef",
    "DataSetSummaryTypeDef",
    "CreateFolderMembershipResponseTypeDef",
    "CreateGroupMembershipResponseTypeDef",
    "DescribeGroupMembershipResponseTypeDef",
    "ListGroupMembershipsResponseTypeDef",
    "CreateGroupResponseTypeDef",
    "DescribeGroupResponseTypeDef",
    "ListGroupsResponseTypeDef",
    "ListUserGroupsResponseTypeDef",
    "SearchGroupsResponseTypeDef",
    "UpdateGroupResponseTypeDef",
    "CreateTemplateAliasResponseTypeDef",
    "DescribeTemplateAliasResponseTypeDef",
    "ListTemplateAliasesResponseTypeDef",
    "UpdateTemplateAliasResponseTypeDef",
    "CreateThemeAliasResponseTypeDef",
    "DescribeThemeAliasResponseTypeDef",
    "ListThemeAliasesResponseTypeDef",
    "UpdateThemeAliasResponseTypeDef",
    "CustomActionNavigationOperationTypeDef",
    "CustomValuesConfigurationTypeDef",
    "CustomSqlTypeDef",
    "RelationalTableTypeDef",
    "SearchDashboardsRequestRequestTypeDef",
    "ListDashboardsResponseTypeDef",
    "SearchDashboardsResponseTypeDef",
    "ListDashboardVersionsResponseTypeDef",
    "DashboardVisualPublishOptionsTypeDef",
    "TableInlineVisualizationTypeDef",
    "DataLabelTypeTypeDef",
    "DataPathColorTypeDef",
    "DataPathSortTypeDef",
    "PivotTableDataPathOptionTypeDef",
    "SearchDataSetsRequestRequestTypeDef",
    "SearchDataSourcesRequestRequestTypeDef",
    "SearchDataSourcesResponseTypeDef",
    "TimeRangeFilterValueTypeDef",
    "DescribeFolderResponseTypeDef",
    "DescribeIAMPolicyAssignmentResponseTypeDef",
    "DescribeUserResponseTypeDef",
    "ListUsersResponseTypeDef",
    "RegisterUserResponseTypeDef",
    "UpdateUserResponseTypeDef",
    "DonutOptionsTypeDef",
    "RelativeDatesFilterTypeDef",
    "FilterOperationTargetVisualsConfigurationTypeDef",
    "SearchFoldersRequestRequestTypeDef",
    "ListFoldersResponseTypeDef",
    "SearchFoldersResponseTypeDef",
    "FontConfigurationTypeDef",
    "TypographyTypeDef",
    "ForecastScenarioTypeDef",
    "FreeFormLayoutCanvasSizeOptionsTypeDef",
    "GeospatialWindowOptionsTypeDef",
    "TableSideBorderOptionsTypeDef",
    "GradientColorTypeDef",
    "GridLayoutCanvasSizeOptionsTypeDef",
    "SearchGroupsRequestRequestTypeDef",
    "ListIAMPolicyAssignmentsResponseTypeDef",
    "IncrementalRefreshTypeDef",
    "IngestionTypeDef",
    "JoinInstructionTypeDef",
    "LineChartDefaultSeriesSettingsTypeDef",
    "LineChartSeriesSettingsTypeDef",
    "ListAnalysesRequestListAnalysesPaginateTypeDef",
    "ListDashboardVersionsRequestListDashboardVersionsPaginateTypeDef",
    "ListDashboardsRequestListDashboardsPaginateTypeDef",
    "ListDataSetsRequestListDataSetsPaginateTypeDef",
    "ListDataSourcesRequestListDataSourcesPaginateTypeDef",
    "ListIngestionsRequestListIngestionsPaginateTypeDef",
    "ListNamespacesRequestListNamespacesPaginateTypeDef",
    "ListTemplateAliasesRequestListTemplateAliasesPaginateTypeDef",
    "ListTemplateVersionsRequestListTemplateVersionsPaginateTypeDef",
    "ListTemplatesRequestListTemplatesPaginateTypeDef",
    "ListThemeVersionsRequestListThemeVersionsPaginateTypeDef",
    "ListThemesRequestListThemesPaginateTypeDef",
    "SearchAnalysesRequestSearchAnalysesPaginateTypeDef",
    "SearchDashboardsRequestSearchDashboardsPaginateTypeDef",
    "SearchDataSetsRequestSearchDataSetsPaginateTypeDef",
    "SearchDataSourcesRequestSearchDataSourcesPaginateTypeDef",
    "ListFolderMembersResponseTypeDef",
    "ListTemplateVersionsResponseTypeDef",
    "ListTemplatesResponseTypeDef",
    "ListThemeVersionsResponseTypeDef",
    "ListThemesResponseTypeDef",
    "VisualSubtitleLabelOptionsTypeDef",
    "S3ParametersTypeDef",
    "TileLayoutStyleTypeDef",
    "NamespaceInfoV2TypeDef",
    "NumericSeparatorConfigurationTypeDef",
    "NumericalAggregationFunctionTypeDef",
    "ParametersTypeDef",
    "VisibleRangeOptionsTypeDef",
    "RadarChartSeriesSettingsTypeDef",
    "RefreshFrequencyTypeDef",
    "RegisteredUserConsoleFeatureConfigurationsTypeDef",
    "RegisteredUserDashboardFeatureConfigurationsTypeDef",
    "RowLevelPermissionTagConfigurationTypeDef",
    "S3SourceTypeDef",
    "SectionPageBreakConfigurationTypeDef",
    "SectionBasedLayoutPaperCanvasSizeOptionsTypeDef",
    "SectionStyleTypeDef",
    "SelectedSheetsFilterScopeConfigurationTypeDef",
    "SheetElementRenderingRuleTypeDef",
    "VisualTitleLabelOptionsTypeDef",
    "TableFieldImageConfigurationTypeDef",
    "CascadingControlConfigurationTypeDef",
    "DateTimeDefaultValuesTypeDef",
    "DecimalDefaultValuesTypeDef",
    "IntegerDefaultValuesTypeDef",
    "StringDefaultValuesTypeDef",
    "DrillDownFilterTypeDef",
    "AnalysisTypeDef",
    "DashboardVersionTypeDef",
    "AnalysisSourceEntityTypeDef",
    "DashboardSourceEntityTypeDef",
    "TemplateSourceEntityTypeDef",
    "AnonymousUserEmbeddingExperienceConfigurationTypeDef",
    "NumericAxisOptionsTypeDef",
    "CategoryFilterTypeDef",
    "ClusterMarkerConfigurationTypeDef",
    "TagColumnOperationTypeDef",
    "DataSetConfigurationTypeDef",
    "ConditionalFormattingIconTypeDef",
    "DescribeDashboardPermissionsResponseTypeDef",
    "UpdateDashboardPermissionsResponseTypeDef",
    "ListDataSetsResponseTypeDef",
    "SearchDataSetsResponseTypeDef",
    "DestinationParameterValueConfigurationTypeDef",
    "DashboardPublishOptionsTypeDef",
    "VisualPaletteTypeDef",
    "PivotTableFieldOptionsTypeDef",
    "TimeRangeFilterTypeDef",
    "CustomActionFilterOperationTypeDef",
    "AxisLabelOptionsTypeDef",
    "DataLabelOptionsTypeDef",
    "FunnelChartDataLabelOptionsTypeDef",
    "LabelOptionsTypeDef",
    "PanelTitleOptionsTypeDef",
    "TableFieldCustomTextContentTypeDef",
    "ForecastConfigurationTypeDef",
    "DefaultFreeFormLayoutConfigurationTypeDef",
    "GlobalTableBorderOptionsTypeDef",
    "ConditionalFormattingGradientColorTypeDef",
    "DefaultGridLayoutConfigurationTypeDef",
    "GridLayoutConfigurationTypeDef",
    "RefreshConfigurationTypeDef",
    "DescribeIngestionResponseTypeDef",
    "ListIngestionsResponseTypeDef",
    "LogicalTableSourceTypeDef",
    "DataFieldSeriesItemTypeDef",
    "FieldSeriesItemTypeDef",
    "DataSourceParametersTypeDef",
    "SheetStyleTypeDef",
    "DescribeNamespaceResponseTypeDef",
    "ListNamespacesResponseTypeDef",
    "CurrencyDisplayFormatConfigurationTypeDef",
    "NumberDisplayFormatConfigurationTypeDef",
    "PercentageDisplayFormatConfigurationTypeDef",
    "AggregationFunctionTypeDef",
    "ScrollBarOptionsTypeDef",
    "RefreshScheduleTypeDef",
    "RegisteredUserQuickSightConsoleEmbeddingConfigurationTypeDef",
    "RegisteredUserDashboardEmbeddingConfigurationTypeDef",
    "PhysicalTableTypeDef",
    "SectionBasedLayoutCanvasSizeOptionsTypeDef",
    "FilterScopeConfigurationTypeDef",
    "FreeFormLayoutElementTypeDef",
    "DateTimeParameterDeclarationTypeDef",
    "DecimalParameterDeclarationTypeDef",
    "IntegerParameterDeclarationTypeDef",
    "StringParameterDeclarationTypeDef",
    "DateTimeHierarchyTypeDef",
    "ExplicitHierarchyTypeDef",
    "PredefinedHierarchyTypeDef",
    "DescribeAnalysisResponseTypeDef",
    "DashboardTypeDef",
    "GenerateEmbedUrlForAnonymousUserRequestRequestTypeDef",
    "AxisDataOptionsTypeDef",
    "GeospatialPointStyleOptionsTypeDef",
    "TransformOperationTypeDef",
    "TemplateVersionTypeDef",
    "SetParameterValueConfigurationTypeDef",
    "ChartAxisLabelOptionsTypeDef",
    "AxisTickLabelOptionsTypeDef",
    "DateTimePickerControlDisplayOptionsTypeDef",
    "DropDownControlDisplayOptionsTypeDef",
    "LegendOptionsTypeDef",
    "ListControlDisplayOptionsTypeDef",
    "RelativeDateTimeControlDisplayOptionsTypeDef",
    "SliderControlDisplayOptionsTypeDef",
    "TextAreaControlDisplayOptionsTypeDef",
    "TextFieldControlDisplayOptionsTypeDef",
    "PanelConfigurationTypeDef",
    "TableFieldLinkContentConfigurationTypeDef",
    "TableCellStyleTypeDef",
    "ConditionalFormattingColorTypeDef",
    "DefaultInteractiveLayoutConfigurationTypeDef",
    "SheetControlLayoutConfigurationTypeDef",
    "DataSetRefreshPropertiesTypeDef",
    "SeriesItemTypeDef",
    "CredentialPairTypeDef",
    "DataSourceTypeDef",
    "ThemeConfigurationTypeDef",
    "ComparisonFormatConfigurationTypeDef",
    "NumericFormatConfigurationTypeDef",
    "AggregationSortConfigurationTypeDef",
    "ColumnSortTypeDef",
    "ColumnTooltipItemTypeDef",
    "NumericEqualityFilterTypeDef",
    "NumericRangeFilterTypeDef",
    "ReferenceLineDynamicDataConfigurationTypeDef",
    "CreateRefreshScheduleRequestRequestTypeDef",
    "DescribeRefreshScheduleResponseTypeDef",
    "ListRefreshSchedulesResponseTypeDef",
    "UpdateRefreshScheduleRequestRequestTypeDef",
    "RegisteredUserEmbeddingExperienceConfigurationTypeDef",
    "DefaultSectionBasedLayoutConfigurationTypeDef",
    "FreeFormLayoutConfigurationTypeDef",
    "FreeFormSectionLayoutConfigurationTypeDef",
    "ParameterDeclarationTypeDef",
    "ColumnHierarchyTypeDef",
    "DescribeDashboardResponseTypeDef",
    "LogicalTableTypeDef",
    "TemplateTypeDef",
    "CustomActionSetParametersOperationTypeDef",
    "AxisDisplayOptionsTypeDef",
    "FilterDateTimePickerControlTypeDef",
    "ParameterDateTimePickerControlTypeDef",
    "FilterDropDownControlTypeDef",
    "ParameterDropDownControlTypeDef",
    "FilterListControlTypeDef",
    "ParameterListControlTypeDef",
    "FilterRelativeDateTimeControlTypeDef",
    "FilterSliderControlTypeDef",
    "ParameterSliderControlTypeDef",
    "FilterTextAreaControlTypeDef",
    "ParameterTextAreaControlTypeDef",
    "FilterTextFieldControlTypeDef",
    "ParameterTextFieldControlTypeDef",
    "SmallMultiplesOptionsTypeDef",
    "TableFieldLinkConfigurationTypeDef",
    "PivotTableOptionsTypeDef",
    "PivotTotalOptionsTypeDef",
    "SubtotalOptionsTypeDef",
    "TableOptionsTypeDef",
    "TotalOptionsTypeDef",
    "GaugeChartArcConditionalFormattingTypeDef",
    "GaugeChartPrimaryValueConditionalFormattingTypeDef",
    "KPIPrimaryValueConditionalFormattingTypeDef",
    "KPIProgressBarConditionalFormattingTypeDef",
    "ShapeConditionalFormatTypeDef",
    "TableRowConditionalFormattingTypeDef",
    "TextConditionalFormatTypeDef",
    "SheetControlLayoutTypeDef",
    "DescribeDataSetRefreshPropertiesResponseTypeDef",
    "PutDataSetRefreshPropertiesRequestRequestTypeDef",
    "DataSourceCredentialsTypeDef",
    "DescribeDataSourceResponseTypeDef",
    "ListDataSourcesResponseTypeDef",
    "CreateThemeRequestRequestTypeDef",
    "ThemeVersionTypeDef",
    "UpdateThemeRequestRequestTypeDef",
    "ComparisonConfigurationTypeDef",
    "DateTimeFormatConfigurationTypeDef",
    "NumberFormatConfigurationTypeDef",
    "ReferenceLineValueLabelConfigurationTypeDef",
    "StringFormatConfigurationTypeDef",
    "TopBottomFilterTypeDef",
    "FieldSortOptionsTypeDef",
    "PivotTableSortByTypeDef",
    "TooltipItemTypeDef",
    "ReferenceLineDataConfigurationTypeDef",
    "GenerateEmbedUrlForRegisteredUserRequestRequestTypeDef",
    "DefaultPaginatedLayoutConfigurationTypeDef",
    "SectionLayoutConfigurationTypeDef",
    "CreateDataSetRequestRequestTypeDef",
    "DataSetTypeDef",
    "UpdateDataSetRequestRequestTypeDef",
    "DescribeTemplateResponseTypeDef",
    "VisualCustomActionOperationTypeDef",
    "LineSeriesAxisDisplayOptionsTypeDef",
    "FilterControlTypeDef",
    "ParameterControlTypeDef",
    "TableFieldURLConfigurationTypeDef",
    "PivotTableTotalOptionsTypeDef",
    "GaugeChartConditionalFormattingOptionTypeDef",
    "KPIConditionalFormattingOptionTypeDef",
    "FilledMapShapeConditionalFormattingTypeDef",
    "PivotTableCellConditionalFormattingTypeDef",
    "TableCellConditionalFormattingTypeDef",
    "CreateDataSourceRequestRequestTypeDef",
    "UpdateDataSourceRequestRequestTypeDef",
    "ThemeTypeDef",
    "GaugeChartOptionsTypeDef",
    "KPIOptionsTypeDef",
    "DateDimensionFieldTypeDef",
    "DateMeasureFieldTypeDef",
    "NumericalDimensionFieldTypeDef",
    "NumericalMeasureFieldTypeDef",
    "ReferenceLineLabelConfigurationTypeDef",
    "CategoricalDimensionFieldTypeDef",
    "CategoricalMeasureFieldTypeDef",
    "FormatConfigurationTypeDef",
    "FilterTypeDef",
    "BarChartSortConfigurationTypeDef",
    "BoxPlotSortConfigurationTypeDef",
    "ComboChartSortConfigurationTypeDef",
    "FilledMapSortConfigurationTypeDef",
    "FunnelChartSortConfigurationTypeDef",
    "HeatMapSortConfigurationTypeDef",
    "KPISortConfigurationTypeDef",
    "LineChartSortConfigurationTypeDef",
    "PieChartSortConfigurationTypeDef",
    "RadarChartSortConfigurationTypeDef",
    "SankeyDiagramSortConfigurationTypeDef",
    "TableSortConfigurationTypeDef",
    "TreeMapSortConfigurationTypeDef",
    "WaterfallChartSortConfigurationTypeDef",
    "WordCloudSortConfigurationTypeDef",
    "PivotFieldSortOptionsTypeDef",
    "FieldBasedTooltipTypeDef",
    "DefaultNewSheetConfigurationTypeDef",
    "BodySectionContentTypeDef",
    "HeaderFooterSectionConfigurationTypeDef",
    "DescribeDataSetResponseTypeDef",
    "VisualCustomActionTypeDef",
    "TableFieldOptionTypeDef",
    "GaugeChartConditionalFormattingTypeDef",
    "KPIConditionalFormattingTypeDef",
    "FilledMapConditionalFormattingOptionTypeDef",
    "PivotTableConditionalFormattingOptionTypeDef",
    "TableConditionalFormattingOptionTypeDef",
    "DescribeThemeResponseTypeDef",
    "ReferenceLineTypeDef",
    "DimensionFieldTypeDef",
    "MeasureFieldTypeDef",
    "ColumnConfigurationTypeDef",
    "UnaggregatedFieldTypeDef",
    "FilterGroupTypeDef",
    "PivotTableSortConfigurationTypeDef",
    "TooltipOptionsTypeDef",
    "AnalysisDefaultsTypeDef",
    "BodySectionConfigurationTypeDef",
    "CustomContentVisualTypeDef",
    "EmptyVisualTypeDef",
    "TableFieldOptionsTypeDef",
    "FilledMapConditionalFormattingTypeDef",
    "PivotTableConditionalFormattingTypeDef",
    "TableConditionalFormattingTypeDef",
    "UniqueValuesComputationTypeDef",
    "BarChartAggregatedFieldWellsTypeDef",
    "BoxPlotAggregatedFieldWellsTypeDef",
    "ComboChartAggregatedFieldWellsTypeDef",
    "FilledMapAggregatedFieldWellsTypeDef",
    "ForecastComputationTypeDef",
    "FunnelChartAggregatedFieldWellsTypeDef",
    "GaugeChartFieldWellsTypeDef",
    "GeospatialMapAggregatedFieldWellsTypeDef",
    "GrowthRateComputationTypeDef",
    "HeatMapAggregatedFieldWellsTypeDef",
    "HistogramAggregatedFieldWellsTypeDef",
    "KPIFieldWellsTypeDef",
    "LineChartAggregatedFieldWellsTypeDef",
    "MaximumMinimumComputationTypeDef",
    "MetricComparisonComputationTypeDef",
    "PeriodOverPeriodComputationTypeDef",
    "PeriodToDateComputationTypeDef",
    "PieChartAggregatedFieldWellsTypeDef",
    "PivotTableAggregatedFieldWellsTypeDef",
    "RadarChartAggregatedFieldWellsTypeDef",
    "SankeyDiagramAggregatedFieldWellsTypeDef",
    "ScatterPlotCategoricallyAggregatedFieldWellsTypeDef",
    "ScatterPlotUnaggregatedFieldWellsTypeDef",
    "TableAggregatedFieldWellsTypeDef",
    "TopBottomMoversComputationTypeDef",
    "TopBottomRankedComputationTypeDef",
    "TotalAggregationComputationTypeDef",
    "TreeMapAggregatedFieldWellsTypeDef",
    "WaterfallChartAggregatedFieldWellsTypeDef",
    "WordCloudAggregatedFieldWellsTypeDef",
    "TableUnaggregatedFieldWellsTypeDef",
    "SectionBasedLayoutConfigurationTypeDef",
    "BarChartFieldWellsTypeDef",
    "BoxPlotFieldWellsTypeDef",
    "ComboChartFieldWellsTypeDef",
    "FilledMapFieldWellsTypeDef",
    "FunnelChartFieldWellsTypeDef",
    "GaugeChartConfigurationTypeDef",
    "GeospatialMapFieldWellsTypeDef",
    "HeatMapFieldWellsTypeDef",
    "HistogramFieldWellsTypeDef",
    "KPIConfigurationTypeDef",
    "LineChartFieldWellsTypeDef",
    "PieChartFieldWellsTypeDef",
    "PivotTableFieldWellsTypeDef",
    "RadarChartFieldWellsTypeDef",
    "SankeyDiagramFieldWellsTypeDef",
    "ScatterPlotFieldWellsTypeDef",
    "ComputationTypeDef",
    "TreeMapFieldWellsTypeDef",
    "WaterfallChartFieldWellsTypeDef",
    "WordCloudFieldWellsTypeDef",
    "TableFieldWellsTypeDef",
    "LayoutConfigurationTypeDef",
    "BarChartConfigurationTypeDef",
    "BoxPlotChartConfigurationTypeDef",
    "ComboChartConfigurationTypeDef",
    "FilledMapConfigurationTypeDef",
    "FunnelChartConfigurationTypeDef",
    "GaugeChartVisualTypeDef",
    "GeospatialMapConfigurationTypeDef",
    "HeatMapConfigurationTypeDef",
    "HistogramConfigurationTypeDef",
    "KPIVisualTypeDef",
    "LineChartConfigurationTypeDef",
    "PieChartConfigurationTypeDef",
    "PivotTableConfigurationTypeDef",
    "RadarChartConfigurationTypeDef",
    "SankeyDiagramChartConfigurationTypeDef",
    "ScatterPlotConfigurationTypeDef",
    "InsightConfigurationTypeDef",
    "TreeMapConfigurationTypeDef",
    "WaterfallChartConfigurationTypeDef",
    "WordCloudChartConfigurationTypeDef",
    "TableConfigurationTypeDef",
    "LayoutTypeDef",
    "BarChartVisualTypeDef",
    "BoxPlotVisualTypeDef",
    "ComboChartVisualTypeDef",
    "FilledMapVisualTypeDef",
    "FunnelChartVisualTypeDef",
    "GeospatialMapVisualTypeDef",
    "HeatMapVisualTypeDef",
    "HistogramVisualTypeDef",
    "LineChartVisualTypeDef",
    "PieChartVisualTypeDef",
    "PivotTableVisualTypeDef",
    "RadarChartVisualTypeDef",
    "SankeyDiagramVisualTypeDef",
    "ScatterPlotVisualTypeDef",
    "InsightVisualTypeDef",
    "TreeMapVisualTypeDef",
    "WaterfallVisualTypeDef",
    "WordCloudVisualTypeDef",
    "TableVisualTypeDef",
    "VisualTypeDef",
    "SheetDefinitionTypeDef",
    "AnalysisDefinitionTypeDef",
    "DashboardVersionDefinitionTypeDef",
    "TemplateVersionDefinitionTypeDef",
    "CreateAnalysisRequestRequestTypeDef",
    "DescribeAnalysisDefinitionResponseTypeDef",
    "UpdateAnalysisRequestRequestTypeDef",
    "CreateDashboardRequestRequestTypeDef",
    "DescribeDashboardDefinitionResponseTypeDef",
    "UpdateDashboardRequestRequestTypeDef",
    "CreateTemplateRequestRequestTypeDef",
    "DescribeTemplateDefinitionResponseTypeDef",
    "UpdateTemplateRequestRequestTypeDef",
)

AccountCustomizationTypeDef = TypedDict(
    "AccountCustomizationTypeDef",
    {
        "DefaultTheme": str,
        "DefaultEmailCustomizationTemplate": str,
    },
    total=False,
)

AccountInfoTypeDef = TypedDict(
    "AccountInfoTypeDef",
    {
        "AccountName": str,
        "Edition": EditionType,
        "NotificationEmail": str,
        "AuthenticationType": str,
        "AccountSubscriptionStatus": str,
    },
    total=False,
)

AccountSettingsTypeDef = TypedDict(
    "AccountSettingsTypeDef",
    {
        "AccountName": str,
        "Edition": EditionType,
        "DefaultNamespace": str,
        "NotificationEmail": str,
        "PublicSharingEnabled": bool,
        "TerminationProtectionEnabled": bool,
    },
    total=False,
)

ActiveIAMPolicyAssignmentTypeDef = TypedDict(
    "ActiveIAMPolicyAssignmentTypeDef",
    {
        "AssignmentName": str,
        "PolicyArn": str,
    },
    total=False,
)

AdHocFilteringOptionTypeDef = TypedDict(
    "AdHocFilteringOptionTypeDef",
    {
        "AvailabilityStatus": DashboardBehaviorType,
    },
    total=False,
)

ColumnIdentifierTypeDef = TypedDict(
    "ColumnIdentifierTypeDef",
    {
        "DataSetIdentifier": str,
        "ColumnName": str,
    },
)

AmazonElasticsearchParametersTypeDef = TypedDict(
    "AmazonElasticsearchParametersTypeDef",
    {
        "Domain": str,
    },
)

AmazonOpenSearchParametersTypeDef = TypedDict(
    "AmazonOpenSearchParametersTypeDef",
    {
        "Domain": str,
    },
)

CalculatedFieldTypeDef = TypedDict(
    "CalculatedFieldTypeDef",
    {
        "DataSetIdentifier": str,
        "Name": str,
        "Expression": str,
    },
)

DataSetIdentifierDeclarationTypeDef = TypedDict(
    "DataSetIdentifierDeclarationTypeDef",
    {
        "Identifier": str,
        "DataSetArn": str,
    },
)

EntityTypeDef = TypedDict(
    "EntityTypeDef",
    {
        "Path": str,
    },
    total=False,
)

AnalysisSearchFilterTypeDef = TypedDict(
    "AnalysisSearchFilterTypeDef",
    {
        "Operator": FilterOperatorType,
        "Name": AnalysisFilterAttributeType,
        "Value": str,
    },
    total=False,
)

DataSetReferenceTypeDef = TypedDict(
    "DataSetReferenceTypeDef",
    {
        "DataSetPlaceholder": str,
        "DataSetArn": str,
    },
)

AnalysisSummaryTypeDef = TypedDict(
    "AnalysisSummaryTypeDef",
    {
        "Arn": str,
        "AnalysisId": str,
        "Name": str,
        "Status": ResourceStatusType,
        "CreatedTime": datetime,
        "LastUpdatedTime": datetime,
    },
    total=False,
)

SheetTypeDef = TypedDict(
    "SheetTypeDef",
    {
        "SheetId": str,
        "Name": str,
    },
    total=False,
)

AnchorDateConfigurationTypeDef = TypedDict(
    "AnchorDateConfigurationTypeDef",
    {
        "AnchorOption": Literal["NOW"],
        "ParameterName": str,
    },
    total=False,
)

AnonymousUserDashboardEmbeddingConfigurationTypeDef = TypedDict(
    "AnonymousUserDashboardEmbeddingConfigurationTypeDef",
    {
        "InitialDashboardId": str,
    },
)

DashboardVisualIdTypeDef = TypedDict(
    "DashboardVisualIdTypeDef",
    {
        "DashboardId": str,
        "SheetId": str,
        "VisualId": str,
    },
)

AnonymousUserQSearchBarEmbeddingConfigurationTypeDef = TypedDict(
    "AnonymousUserQSearchBarEmbeddingConfigurationTypeDef",
    {
        "InitialTopicId": str,
    },
)

ArcAxisDisplayRangeTypeDef = TypedDict(
    "ArcAxisDisplayRangeTypeDef",
    {
        "Min": float,
        "Max": float,
    },
    total=False,
)

ArcConfigurationTypeDef = TypedDict(
    "ArcConfigurationTypeDef",
    {
        "ArcAngle": float,
        "ArcThickness": ArcThicknessOptionsType,
    },
    total=False,
)

ArcOptionsTypeDef = TypedDict(
    "ArcOptionsTypeDef",
    {
        "ArcThickness": ArcThicknessType,
    },
    total=False,
)

AthenaParametersTypeDef = TypedDict(
    "AthenaParametersTypeDef",
    {
        "WorkGroup": str,
        "RoleArn": str,
    },
    total=False,
)

AuroraParametersTypeDef = TypedDict(
    "AuroraParametersTypeDef",
    {
        "Host": str,
        "Port": int,
        "Database": str,
    },
)

AuroraPostgreSqlParametersTypeDef = TypedDict(
    "AuroraPostgreSqlParametersTypeDef",
    {
        "Host": str,
        "Port": int,
        "Database": str,
    },
)

AwsIotAnalyticsParametersTypeDef = TypedDict(
    "AwsIotAnalyticsParametersTypeDef",
    {
        "DataSetName": str,
    },
)

DateAxisOptionsTypeDef = TypedDict(
    "DateAxisOptionsTypeDef",
    {
        "MissingDateVisibility": VisibilityType,
    },
    total=False,
)

AxisDisplayMinMaxRangeTypeDef = TypedDict(
    "AxisDisplayMinMaxRangeTypeDef",
    {
        "Minimum": float,
        "Maximum": float,
    },
    total=False,
)

AxisLinearScaleTypeDef = TypedDict(
    "AxisLinearScaleTypeDef",
    {
        "StepCount": int,
        "StepSize": float,
    },
    total=False,
)

AxisLogarithmicScaleTypeDef = TypedDict(
    "AxisLogarithmicScaleTypeDef",
    {
        "Base": float,
    },
    total=False,
)

ItemsLimitConfigurationTypeDef = TypedDict(
    "ItemsLimitConfigurationTypeDef",
    {
        "ItemsLimit": int,
        "OtherCategories": OtherCategoriesType,
    },
    total=False,
)

BinCountOptionsTypeDef = TypedDict(
    "BinCountOptionsTypeDef",
    {
        "Value": int,
    },
    total=False,
)

BinWidthOptionsTypeDef = TypedDict(
    "BinWidthOptionsTypeDef",
    {
        "Value": float,
        "BinCountLimit": int,
    },
    total=False,
)

BorderStyleTypeDef = TypedDict(
    "BorderStyleTypeDef",
    {
        "Show": bool,
    },
    total=False,
)

BoxPlotStyleOptionsTypeDef = TypedDict(
    "BoxPlotStyleOptionsTypeDef",
    {
        "FillStyle": BoxPlotFillStyleType,
    },
    total=False,
)

PaginationConfigurationTypeDef = TypedDict(
    "PaginationConfigurationTypeDef",
    {
        "PageSize": int,
        "PageNumber": int,
    },
)

CalculatedColumnTypeDef = TypedDict(
    "CalculatedColumnTypeDef",
    {
        "ColumnName": str,
        "ColumnId": str,
        "Expression": str,
    },
)

CalculatedMeasureFieldTypeDef = TypedDict(
    "CalculatedMeasureFieldTypeDef",
    {
        "FieldId": str,
        "Expression": str,
    },
)

CancelIngestionRequestRequestTypeDef = TypedDict(
    "CancelIngestionRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DataSetId": str,
        "IngestionId": str,
    },
)

ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HostId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
    },
)

_RequiredCastColumnTypeOperationTypeDef = TypedDict(
    "_RequiredCastColumnTypeOperationTypeDef",
    {
        "ColumnName": str,
        "NewColumnType": ColumnDataTypeType,
    },
)
_OptionalCastColumnTypeOperationTypeDef = TypedDict(
    "_OptionalCastColumnTypeOperationTypeDef",
    {
        "Format": str,
    },
    total=False,
)


class CastColumnTypeOperationTypeDef(
    _RequiredCastColumnTypeOperationTypeDef, _OptionalCastColumnTypeOperationTypeDef
):
    pass


_RequiredCustomFilterConfigurationTypeDef = TypedDict(
    "_RequiredCustomFilterConfigurationTypeDef",
    {
        "MatchOperator": CategoryFilterMatchOperatorType,
        "NullOption": FilterNullOptionType,
    },
)
_OptionalCustomFilterConfigurationTypeDef = TypedDict(
    "_OptionalCustomFilterConfigurationTypeDef",
    {
        "CategoryValue": str,
        "SelectAllOptions": Literal["FILTER_ALL_VALUES"],
        "ParameterName": str,
    },
    total=False,
)


class CustomFilterConfigurationTypeDef(
    _RequiredCustomFilterConfigurationTypeDef, _OptionalCustomFilterConfigurationTypeDef
):
    pass


_RequiredCustomFilterListConfigurationTypeDef = TypedDict(
    "_RequiredCustomFilterListConfigurationTypeDef",
    {
        "MatchOperator": CategoryFilterMatchOperatorType,
        "NullOption": FilterNullOptionType,
    },
)
_OptionalCustomFilterListConfigurationTypeDef = TypedDict(
    "_OptionalCustomFilterListConfigurationTypeDef",
    {
        "CategoryValues": Sequence[str],
        "SelectAllOptions": Literal["FILTER_ALL_VALUES"],
    },
    total=False,
)


class CustomFilterListConfigurationTypeDef(
    _RequiredCustomFilterListConfigurationTypeDef, _OptionalCustomFilterListConfigurationTypeDef
):
    pass


_RequiredFilterListConfigurationTypeDef = TypedDict(
    "_RequiredFilterListConfigurationTypeDef",
    {
        "MatchOperator": CategoryFilterMatchOperatorType,
    },
)
_OptionalFilterListConfigurationTypeDef = TypedDict(
    "_OptionalFilterListConfigurationTypeDef",
    {
        "CategoryValues": Sequence[str],
        "SelectAllOptions": Literal["FILTER_ALL_VALUES"],
    },
    total=False,
)


class FilterListConfigurationTypeDef(
    _RequiredFilterListConfigurationTypeDef, _OptionalFilterListConfigurationTypeDef
):
    pass


SimpleClusterMarkerTypeDef = TypedDict(
    "SimpleClusterMarkerTypeDef",
    {
        "Color": str,
    },
    total=False,
)

DataColorTypeDef = TypedDict(
    "DataColorTypeDef",
    {
        "Color": str,
        "DataValue": float,
    },
    total=False,
)

ColumnDescriptionTypeDef = TypedDict(
    "ColumnDescriptionTypeDef",
    {
        "Text": str,
    },
    total=False,
)

ColumnGroupColumnSchemaTypeDef = TypedDict(
    "ColumnGroupColumnSchemaTypeDef",
    {
        "Name": str,
    },
    total=False,
)

_RequiredGeoSpatialColumnGroupTypeDef = TypedDict(
    "_RequiredGeoSpatialColumnGroupTypeDef",
    {
        "Name": str,
        "Columns": Sequence[str],
    },
)
_OptionalGeoSpatialColumnGroupTypeDef = TypedDict(
    "_OptionalGeoSpatialColumnGroupTypeDef",
    {
        "CountryCode": Literal["US"],
    },
    total=False,
)


class GeoSpatialColumnGroupTypeDef(
    _RequiredGeoSpatialColumnGroupTypeDef, _OptionalGeoSpatialColumnGroupTypeDef
):
    pass


ColumnLevelPermissionRuleTypeDef = TypedDict(
    "ColumnLevelPermissionRuleTypeDef",
    {
        "Principals": Sequence[str],
        "ColumnNames": Sequence[str],
    },
    total=False,
)

ColumnSchemaTypeDef = TypedDict(
    "ColumnSchemaTypeDef",
    {
        "Name": str,
        "DataType": str,
        "GeographicRole": str,
    },
    total=False,
)

_RequiredConditionalFormattingSolidColorTypeDef = TypedDict(
    "_RequiredConditionalFormattingSolidColorTypeDef",
    {
        "Expression": str,
    },
)
_OptionalConditionalFormattingSolidColorTypeDef = TypedDict(
    "_OptionalConditionalFormattingSolidColorTypeDef",
    {
        "Color": str,
    },
    total=False,
)


class ConditionalFormattingSolidColorTypeDef(
    _RequiredConditionalFormattingSolidColorTypeDef, _OptionalConditionalFormattingSolidColorTypeDef
):
    pass


ConditionalFormattingCustomIconOptionsTypeDef = TypedDict(
    "ConditionalFormattingCustomIconOptionsTypeDef",
    {
        "Icon": IconType,
        "UnicodeIcon": str,
    },
    total=False,
)

ConditionalFormattingIconDisplayConfigurationTypeDef = TypedDict(
    "ConditionalFormattingIconDisplayConfigurationTypeDef",
    {
        "IconDisplayOption": Literal["ICON_ONLY"],
    },
    total=False,
)

_RequiredConditionalFormattingIconSetTypeDef = TypedDict(
    "_RequiredConditionalFormattingIconSetTypeDef",
    {
        "Expression": str,
    },
)
_OptionalConditionalFormattingIconSetTypeDef = TypedDict(
    "_OptionalConditionalFormattingIconSetTypeDef",
    {
        "IconSetType": ConditionalFormattingIconSetTypeType,
    },
    total=False,
)


class ConditionalFormattingIconSetTypeDef(
    _RequiredConditionalFormattingIconSetTypeDef, _OptionalConditionalFormattingIconSetTypeDef
):
    pass


TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

_RequiredCreateAccountSubscriptionRequestRequestTypeDef = TypedDict(
    "_RequiredCreateAccountSubscriptionRequestRequestTypeDef",
    {
        "Edition": EditionType,
        "AuthenticationMethod": AuthenticationMethodOptionType,
        "AwsAccountId": str,
        "AccountName": str,
        "NotificationEmail": str,
    },
)
_OptionalCreateAccountSubscriptionRequestRequestTypeDef = TypedDict(
    "_OptionalCreateAccountSubscriptionRequestRequestTypeDef",
    {
        "ActiveDirectoryName": str,
        "Realm": str,
        "DirectoryId": str,
        "AdminGroup": Sequence[str],
        "AuthorGroup": Sequence[str],
        "ReaderGroup": Sequence[str],
        "FirstName": str,
        "LastName": str,
        "EmailAddress": str,
        "ContactNumber": str,
    },
    total=False,
)


class CreateAccountSubscriptionRequestRequestTypeDef(
    _RequiredCreateAccountSubscriptionRequestRequestTypeDef,
    _OptionalCreateAccountSubscriptionRequestRequestTypeDef,
):
    pass


SignupResponseTypeDef = TypedDict(
    "SignupResponseTypeDef",
    {
        "IAMUser": bool,
        "userLoginName": str,
        "accountName": str,
        "directoryType": str,
    },
    total=False,
)

ResourcePermissionTypeDef = TypedDict(
    "ResourcePermissionTypeDef",
    {
        "Principal": str,
        "Actions": Sequence[str],
    },
)

DataSetUsageConfigurationTypeDef = TypedDict(
    "DataSetUsageConfigurationTypeDef",
    {
        "DisableUseAsDirectQuerySource": bool,
        "DisableUseAsImportedSource": bool,
    },
    total=False,
)

FieldFolderTypeDef = TypedDict(
    "FieldFolderTypeDef",
    {
        "description": str,
        "columns": Sequence[str],
    },
    total=False,
)

_RequiredRowLevelPermissionDataSetTypeDef = TypedDict(
    "_RequiredRowLevelPermissionDataSetTypeDef",
    {
        "Arn": str,
        "PermissionPolicy": RowLevelPermissionPolicyType,
    },
)
_OptionalRowLevelPermissionDataSetTypeDef = TypedDict(
    "_OptionalRowLevelPermissionDataSetTypeDef",
    {
        "Namespace": str,
        "FormatVersion": RowLevelPermissionFormatVersionType,
        "Status": StatusType,
    },
    total=False,
)


class RowLevelPermissionDataSetTypeDef(
    _RequiredRowLevelPermissionDataSetTypeDef, _OptionalRowLevelPermissionDataSetTypeDef
):
    pass


SslPropertiesTypeDef = TypedDict(
    "SslPropertiesTypeDef",
    {
        "DisableSsl": bool,
    },
    total=False,
)

VpcConnectionPropertiesTypeDef = TypedDict(
    "VpcConnectionPropertiesTypeDef",
    {
        "VpcConnectionArn": str,
    },
)

CreateFolderMembershipRequestRequestTypeDef = TypedDict(
    "CreateFolderMembershipRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "FolderId": str,
        "MemberId": str,
        "MemberType": MemberTypeType,
    },
)

FolderMemberTypeDef = TypedDict(
    "FolderMemberTypeDef",
    {
        "MemberId": str,
        "MemberType": MemberTypeType,
    },
    total=False,
)

CreateGroupMembershipRequestRequestTypeDef = TypedDict(
    "CreateGroupMembershipRequestRequestTypeDef",
    {
        "MemberName": str,
        "GroupName": str,
        "AwsAccountId": str,
        "Namespace": str,
    },
)

GroupMemberTypeDef = TypedDict(
    "GroupMemberTypeDef",
    {
        "Arn": str,
        "MemberName": str,
    },
    total=False,
)

_RequiredCreateGroupRequestRequestTypeDef = TypedDict(
    "_RequiredCreateGroupRequestRequestTypeDef",
    {
        "GroupName": str,
        "AwsAccountId": str,
        "Namespace": str,
    },
)
_OptionalCreateGroupRequestRequestTypeDef = TypedDict(
    "_OptionalCreateGroupRequestRequestTypeDef",
    {
        "Description": str,
    },
    total=False,
)


class CreateGroupRequestRequestTypeDef(
    _RequiredCreateGroupRequestRequestTypeDef, _OptionalCreateGroupRequestRequestTypeDef
):
    pass


GroupTypeDef = TypedDict(
    "GroupTypeDef",
    {
        "Arn": str,
        "GroupName": str,
        "Description": str,
        "PrincipalId": str,
    },
    total=False,
)

_RequiredCreateIAMPolicyAssignmentRequestRequestTypeDef = TypedDict(
    "_RequiredCreateIAMPolicyAssignmentRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "AssignmentName": str,
        "AssignmentStatus": AssignmentStatusType,
        "Namespace": str,
    },
)
_OptionalCreateIAMPolicyAssignmentRequestRequestTypeDef = TypedDict(
    "_OptionalCreateIAMPolicyAssignmentRequestRequestTypeDef",
    {
        "PolicyArn": str,
        "Identities": Mapping[str, Sequence[str]],
    },
    total=False,
)


class CreateIAMPolicyAssignmentRequestRequestTypeDef(
    _RequiredCreateIAMPolicyAssignmentRequestRequestTypeDef,
    _OptionalCreateIAMPolicyAssignmentRequestRequestTypeDef,
):
    pass


_RequiredCreateIngestionRequestRequestTypeDef = TypedDict(
    "_RequiredCreateIngestionRequestRequestTypeDef",
    {
        "DataSetId": str,
        "IngestionId": str,
        "AwsAccountId": str,
    },
)
_OptionalCreateIngestionRequestRequestTypeDef = TypedDict(
    "_OptionalCreateIngestionRequestRequestTypeDef",
    {
        "IngestionType": IngestionTypeType,
    },
    total=False,
)


class CreateIngestionRequestRequestTypeDef(
    _RequiredCreateIngestionRequestRequestTypeDef, _OptionalCreateIngestionRequestRequestTypeDef
):
    pass


CreateTemplateAliasRequestRequestTypeDef = TypedDict(
    "CreateTemplateAliasRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "TemplateId": str,
        "AliasName": str,
        "TemplateVersionNumber": int,
    },
)

TemplateAliasTypeDef = TypedDict(
    "TemplateAliasTypeDef",
    {
        "AliasName": str,
        "Arn": str,
        "TemplateVersionNumber": int,
    },
    total=False,
)

CreateThemeAliasRequestRequestTypeDef = TypedDict(
    "CreateThemeAliasRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "ThemeId": str,
        "AliasName": str,
        "ThemeVersionNumber": int,
    },
)

ThemeAliasTypeDef = TypedDict(
    "ThemeAliasTypeDef",
    {
        "Arn": str,
        "AliasName": str,
        "ThemeVersionNumber": int,
    },
    total=False,
)

DecimalPlacesConfigurationTypeDef = TypedDict(
    "DecimalPlacesConfigurationTypeDef",
    {
        "DecimalPlaces": int,
    },
)

NegativeValueConfigurationTypeDef = TypedDict(
    "NegativeValueConfigurationTypeDef",
    {
        "DisplayMode": NegativeValueDisplayModeType,
    },
)

NullValueFormatConfigurationTypeDef = TypedDict(
    "NullValueFormatConfigurationTypeDef",
    {
        "NullString": str,
    },
)

FilterOperationSelectedFieldsConfigurationTypeDef = TypedDict(
    "FilterOperationSelectedFieldsConfigurationTypeDef",
    {
        "SelectedFields": Sequence[str],
        "SelectedFieldOptions": Literal["ALL_FIELDS"],
    },
    total=False,
)

LocalNavigationConfigurationTypeDef = TypedDict(
    "LocalNavigationConfigurationTypeDef",
    {
        "TargetSheetId": str,
    },
)

CustomActionURLOperationTypeDef = TypedDict(
    "CustomActionURLOperationTypeDef",
    {
        "URLTemplate": str,
        "URLTarget": URLTargetConfigurationType,
    },
)

CustomContentConfigurationTypeDef = TypedDict(
    "CustomContentConfigurationTypeDef",
    {
        "ContentUrl": str,
        "ContentType": CustomContentTypeType,
        "ImageScaling": CustomContentImageScalingConfigurationType,
    },
    total=False,
)

CustomNarrativeOptionsTypeDef = TypedDict(
    "CustomNarrativeOptionsTypeDef",
    {
        "Narrative": str,
    },
)

CustomParameterValuesTypeDef = TypedDict(
    "CustomParameterValuesTypeDef",
    {
        "StringValues": Sequence[str],
        "IntegerValues": Sequence[int],
        "DecimalValues": Sequence[float],
        "DateTimeValues": Sequence[Union[datetime, str]],
    },
    total=False,
)

InputColumnTypeDef = TypedDict(
    "InputColumnTypeDef",
    {
        "Name": str,
        "Type": InputColumnDataTypeType,
    },
)

DataPointDrillUpDownOptionTypeDef = TypedDict(
    "DataPointDrillUpDownOptionTypeDef",
    {
        "AvailabilityStatus": DashboardBehaviorType,
    },
    total=False,
)

DataPointMenuLabelOptionTypeDef = TypedDict(
    "DataPointMenuLabelOptionTypeDef",
    {
        "AvailabilityStatus": DashboardBehaviorType,
    },
    total=False,
)

DataPointTooltipOptionTypeDef = TypedDict(
    "DataPointTooltipOptionTypeDef",
    {
        "AvailabilityStatus": DashboardBehaviorType,
    },
    total=False,
)

ExportToCSVOptionTypeDef = TypedDict(
    "ExportToCSVOptionTypeDef",
    {
        "AvailabilityStatus": DashboardBehaviorType,
    },
    total=False,
)

ExportWithHiddenFieldsOptionTypeDef = TypedDict(
    "ExportWithHiddenFieldsOptionTypeDef",
    {
        "AvailabilityStatus": DashboardBehaviorType,
    },
    total=False,
)

SheetControlsOptionTypeDef = TypedDict(
    "SheetControlsOptionTypeDef",
    {
        "VisibilityState": DashboardUIStateType,
    },
    total=False,
)

SheetLayoutElementMaximizationOptionTypeDef = TypedDict(
    "SheetLayoutElementMaximizationOptionTypeDef",
    {
        "AvailabilityStatus": DashboardBehaviorType,
    },
    total=False,
)

VisualAxisSortOptionTypeDef = TypedDict(
    "VisualAxisSortOptionTypeDef",
    {
        "AvailabilityStatus": DashboardBehaviorType,
    },
    total=False,
)

VisualMenuOptionTypeDef = TypedDict(
    "VisualMenuOptionTypeDef",
    {
        "AvailabilityStatus": DashboardBehaviorType,
    },
    total=False,
)

_RequiredDashboardSearchFilterTypeDef = TypedDict(
    "_RequiredDashboardSearchFilterTypeDef",
    {
        "Operator": FilterOperatorType,
    },
)
_OptionalDashboardSearchFilterTypeDef = TypedDict(
    "_OptionalDashboardSearchFilterTypeDef",
    {
        "Name": DashboardFilterAttributeType,
        "Value": str,
    },
    total=False,
)


class DashboardSearchFilterTypeDef(
    _RequiredDashboardSearchFilterTypeDef, _OptionalDashboardSearchFilterTypeDef
):
    pass


DashboardSummaryTypeDef = TypedDict(
    "DashboardSummaryTypeDef",
    {
        "Arn": str,
        "DashboardId": str,
        "Name": str,
        "CreatedTime": datetime,
        "LastUpdatedTime": datetime,
        "PublishedVersionNumber": int,
        "LastPublishedTime": datetime,
    },
    total=False,
)

DashboardVersionSummaryTypeDef = TypedDict(
    "DashboardVersionSummaryTypeDef",
    {
        "Arn": str,
        "CreatedTime": datetime,
        "VersionNumber": int,
        "Status": ResourceStatusType,
        "SourceEntityArn": str,
        "Description": str,
    },
    total=False,
)

ExportHiddenFieldsOptionTypeDef = TypedDict(
    "ExportHiddenFieldsOptionTypeDef",
    {
        "AvailabilityStatus": DashboardBehaviorType,
    },
    total=False,
)

_RequiredDataBarsOptionsTypeDef = TypedDict(
    "_RequiredDataBarsOptionsTypeDef",
    {
        "FieldId": str,
    },
)
_OptionalDataBarsOptionsTypeDef = TypedDict(
    "_OptionalDataBarsOptionsTypeDef",
    {
        "PositiveColor": str,
        "NegativeColor": str,
    },
    total=False,
)


class DataBarsOptionsTypeDef(_RequiredDataBarsOptionsTypeDef, _OptionalDataBarsOptionsTypeDef):
    pass


DataColorPaletteTypeDef = TypedDict(
    "DataColorPaletteTypeDef",
    {
        "Colors": Sequence[str],
        "MinMaxGradient": Sequence[str],
        "EmptyFillColor": str,
    },
    total=False,
)

DataPathLabelTypeTypeDef = TypedDict(
    "DataPathLabelTypeTypeDef",
    {
        "FieldId": str,
        "FieldValue": str,
        "Visibility": VisibilityType,
    },
    total=False,
)

FieldLabelTypeTypeDef = TypedDict(
    "FieldLabelTypeTypeDef",
    {
        "FieldId": str,
        "Visibility": VisibilityType,
    },
    total=False,
)

MaximumLabelTypeTypeDef = TypedDict(
    "MaximumLabelTypeTypeDef",
    {
        "Visibility": VisibilityType,
    },
    total=False,
)

MinimumLabelTypeTypeDef = TypedDict(
    "MinimumLabelTypeTypeDef",
    {
        "Visibility": VisibilityType,
    },
    total=False,
)

RangeEndsLabelTypeTypeDef = TypedDict(
    "RangeEndsLabelTypeTypeDef",
    {
        "Visibility": VisibilityType,
    },
    total=False,
)

DataPathValueTypeDef = TypedDict(
    "DataPathValueTypeDef",
    {
        "FieldId": str,
        "FieldValue": str,
    },
)

DataSetSearchFilterTypeDef = TypedDict(
    "DataSetSearchFilterTypeDef",
    {
        "Operator": FilterOperatorType,
        "Name": DataSetFilterAttributeType,
        "Value": str,
    },
)

OutputColumnTypeDef = TypedDict(
    "OutputColumnTypeDef",
    {
        "Name": str,
        "Description": str,
        "Type": ColumnDataTypeType,
    },
    total=False,
)

DataSourceErrorInfoTypeDef = TypedDict(
    "DataSourceErrorInfoTypeDef",
    {
        "Type": DataSourceErrorInfoTypeType,
        "Message": str,
    },
    total=False,
)

DatabricksParametersTypeDef = TypedDict(
    "DatabricksParametersTypeDef",
    {
        "Host": str,
        "Port": int,
        "SqlEndpointPath": str,
    },
)

ExasolParametersTypeDef = TypedDict(
    "ExasolParametersTypeDef",
    {
        "Host": str,
        "Port": int,
    },
)

JiraParametersTypeDef = TypedDict(
    "JiraParametersTypeDef",
    {
        "SiteBaseUrl": str,
    },
)

MariaDbParametersTypeDef = TypedDict(
    "MariaDbParametersTypeDef",
    {
        "Host": str,
        "Port": int,
        "Database": str,
    },
)

MySqlParametersTypeDef = TypedDict(
    "MySqlParametersTypeDef",
    {
        "Host": str,
        "Port": int,
        "Database": str,
    },
)

OracleParametersTypeDef = TypedDict(
    "OracleParametersTypeDef",
    {
        "Host": str,
        "Port": int,
        "Database": str,
    },
)

PostgreSqlParametersTypeDef = TypedDict(
    "PostgreSqlParametersTypeDef",
    {
        "Host": str,
        "Port": int,
        "Database": str,
    },
)

PrestoParametersTypeDef = TypedDict(
    "PrestoParametersTypeDef",
    {
        "Host": str,
        "Port": int,
        "Catalog": str,
    },
)

RdsParametersTypeDef = TypedDict(
    "RdsParametersTypeDef",
    {
        "InstanceId": str,
        "Database": str,
    },
)

_RequiredRedshiftParametersTypeDef = TypedDict(
    "_RequiredRedshiftParametersTypeDef",
    {
        "Database": str,
    },
)
_OptionalRedshiftParametersTypeDef = TypedDict(
    "_OptionalRedshiftParametersTypeDef",
    {
        "Host": str,
        "Port": int,
        "ClusterId": str,
    },
    total=False,
)


class RedshiftParametersTypeDef(
    _RequiredRedshiftParametersTypeDef, _OptionalRedshiftParametersTypeDef
):
    pass


ServiceNowParametersTypeDef = TypedDict(
    "ServiceNowParametersTypeDef",
    {
        "SiteBaseUrl": str,
    },
)

SnowflakeParametersTypeDef = TypedDict(
    "SnowflakeParametersTypeDef",
    {
        "Host": str,
        "Database": str,
        "Warehouse": str,
    },
)

SparkParametersTypeDef = TypedDict(
    "SparkParametersTypeDef",
    {
        "Host": str,
        "Port": int,
    },
)

SqlServerParametersTypeDef = TypedDict(
    "SqlServerParametersTypeDef",
    {
        "Host": str,
        "Port": int,
        "Database": str,
    },
)

TeradataParametersTypeDef = TypedDict(
    "TeradataParametersTypeDef",
    {
        "Host": str,
        "Port": int,
        "Database": str,
    },
)

TwitterParametersTypeDef = TypedDict(
    "TwitterParametersTypeDef",
    {
        "Query": str,
        "MaxRows": int,
    },
)

DataSourceSearchFilterTypeDef = TypedDict(
    "DataSourceSearchFilterTypeDef",
    {
        "Operator": FilterOperatorType,
        "Name": DataSourceFilterAttributeType,
        "Value": str,
    },
)

DataSourceSummaryTypeDef = TypedDict(
    "DataSourceSummaryTypeDef",
    {
        "Arn": str,
        "DataSourceId": str,
        "Name": str,
        "Type": DataSourceTypeType,
        "CreatedTime": datetime,
        "LastUpdatedTime": datetime,
    },
    total=False,
)

_RequiredRollingDateConfigurationTypeDef = TypedDict(
    "_RequiredRollingDateConfigurationTypeDef",
    {
        "Expression": str,
    },
)
_OptionalRollingDateConfigurationTypeDef = TypedDict(
    "_OptionalRollingDateConfigurationTypeDef",
    {
        "DataSetIdentifier": str,
    },
    total=False,
)


class RollingDateConfigurationTypeDef(
    _RequiredRollingDateConfigurationTypeDef, _OptionalRollingDateConfigurationTypeDef
):
    pass


DateTimeValueWhenUnsetConfigurationTypeDef = TypedDict(
    "DateTimeValueWhenUnsetConfigurationTypeDef",
    {
        "ValueWhenUnsetOption": ValueWhenUnsetOptionType,
        "CustomValue": Union[datetime, str],
    },
    total=False,
)

DateTimeParameterTypeDef = TypedDict(
    "DateTimeParameterTypeDef",
    {
        "Name": str,
        "Values": Sequence[Union[datetime, str]],
    },
)

DecimalValueWhenUnsetConfigurationTypeDef = TypedDict(
    "DecimalValueWhenUnsetConfigurationTypeDef",
    {
        "ValueWhenUnsetOption": ValueWhenUnsetOptionType,
        "CustomValue": float,
    },
    total=False,
)

DecimalParameterTypeDef = TypedDict(
    "DecimalParameterTypeDef",
    {
        "Name": str,
        "Values": Sequence[float],
    },
)

_RequiredDeleteAccountCustomizationRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteAccountCustomizationRequestRequestTypeDef",
    {
        "AwsAccountId": str,
    },
)
_OptionalDeleteAccountCustomizationRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteAccountCustomizationRequestRequestTypeDef",
    {
        "Namespace": str,
    },
    total=False,
)


class DeleteAccountCustomizationRequestRequestTypeDef(
    _RequiredDeleteAccountCustomizationRequestRequestTypeDef,
    _OptionalDeleteAccountCustomizationRequestRequestTypeDef,
):
    pass


DeleteAccountSubscriptionRequestRequestTypeDef = TypedDict(
    "DeleteAccountSubscriptionRequestRequestTypeDef",
    {
        "AwsAccountId": str,
    },
)

_RequiredDeleteAnalysisRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteAnalysisRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "AnalysisId": str,
    },
)
_OptionalDeleteAnalysisRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteAnalysisRequestRequestTypeDef",
    {
        "RecoveryWindowInDays": int,
        "ForceDeleteWithoutRecovery": bool,
    },
    total=False,
)


class DeleteAnalysisRequestRequestTypeDef(
    _RequiredDeleteAnalysisRequestRequestTypeDef, _OptionalDeleteAnalysisRequestRequestTypeDef
):
    pass


_RequiredDeleteDashboardRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteDashboardRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DashboardId": str,
    },
)
_OptionalDeleteDashboardRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteDashboardRequestRequestTypeDef",
    {
        "VersionNumber": int,
    },
    total=False,
)


class DeleteDashboardRequestRequestTypeDef(
    _RequiredDeleteDashboardRequestRequestTypeDef, _OptionalDeleteDashboardRequestRequestTypeDef
):
    pass


DeleteDataSetRefreshPropertiesRequestRequestTypeDef = TypedDict(
    "DeleteDataSetRefreshPropertiesRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DataSetId": str,
    },
)

DeleteDataSetRequestRequestTypeDef = TypedDict(
    "DeleteDataSetRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DataSetId": str,
    },
)

DeleteDataSourceRequestRequestTypeDef = TypedDict(
    "DeleteDataSourceRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DataSourceId": str,
    },
)

DeleteFolderMembershipRequestRequestTypeDef = TypedDict(
    "DeleteFolderMembershipRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "FolderId": str,
        "MemberId": str,
        "MemberType": MemberTypeType,
    },
)

DeleteFolderRequestRequestTypeDef = TypedDict(
    "DeleteFolderRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "FolderId": str,
    },
)

DeleteGroupMembershipRequestRequestTypeDef = TypedDict(
    "DeleteGroupMembershipRequestRequestTypeDef",
    {
        "MemberName": str,
        "GroupName": str,
        "AwsAccountId": str,
        "Namespace": str,
    },
)

DeleteGroupRequestRequestTypeDef = TypedDict(
    "DeleteGroupRequestRequestTypeDef",
    {
        "GroupName": str,
        "AwsAccountId": str,
        "Namespace": str,
    },
)

DeleteIAMPolicyAssignmentRequestRequestTypeDef = TypedDict(
    "DeleteIAMPolicyAssignmentRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "AssignmentName": str,
        "Namespace": str,
    },
)

DeleteNamespaceRequestRequestTypeDef = TypedDict(
    "DeleteNamespaceRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "Namespace": str,
    },
)

DeleteRefreshScheduleRequestRequestTypeDef = TypedDict(
    "DeleteRefreshScheduleRequestRequestTypeDef",
    {
        "DataSetId": str,
        "AwsAccountId": str,
        "ScheduleId": str,
    },
)

DeleteTemplateAliasRequestRequestTypeDef = TypedDict(
    "DeleteTemplateAliasRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "TemplateId": str,
        "AliasName": str,
    },
)

_RequiredDeleteTemplateRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteTemplateRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "TemplateId": str,
    },
)
_OptionalDeleteTemplateRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteTemplateRequestRequestTypeDef",
    {
        "VersionNumber": int,
    },
    total=False,
)


class DeleteTemplateRequestRequestTypeDef(
    _RequiredDeleteTemplateRequestRequestTypeDef, _OptionalDeleteTemplateRequestRequestTypeDef
):
    pass


DeleteThemeAliasRequestRequestTypeDef = TypedDict(
    "DeleteThemeAliasRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "ThemeId": str,
        "AliasName": str,
    },
)

_RequiredDeleteThemeRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteThemeRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "ThemeId": str,
    },
)
_OptionalDeleteThemeRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteThemeRequestRequestTypeDef",
    {
        "VersionNumber": int,
    },
    total=False,
)


class DeleteThemeRequestRequestTypeDef(
    _RequiredDeleteThemeRequestRequestTypeDef, _OptionalDeleteThemeRequestRequestTypeDef
):
    pass


DeleteUserByPrincipalIdRequestRequestTypeDef = TypedDict(
    "DeleteUserByPrincipalIdRequestRequestTypeDef",
    {
        "PrincipalId": str,
        "AwsAccountId": str,
        "Namespace": str,
    },
)

DeleteUserRequestRequestTypeDef = TypedDict(
    "DeleteUserRequestRequestTypeDef",
    {
        "UserName": str,
        "AwsAccountId": str,
        "Namespace": str,
    },
)

_RequiredDescribeAccountCustomizationRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeAccountCustomizationRequestRequestTypeDef",
    {
        "AwsAccountId": str,
    },
)
_OptionalDescribeAccountCustomizationRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeAccountCustomizationRequestRequestTypeDef",
    {
        "Namespace": str,
        "Resolved": bool,
    },
    total=False,
)


class DescribeAccountCustomizationRequestRequestTypeDef(
    _RequiredDescribeAccountCustomizationRequestRequestTypeDef,
    _OptionalDescribeAccountCustomizationRequestRequestTypeDef,
):
    pass


DescribeAccountSettingsRequestRequestTypeDef = TypedDict(
    "DescribeAccountSettingsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
    },
)

DescribeAccountSubscriptionRequestRequestTypeDef = TypedDict(
    "DescribeAccountSubscriptionRequestRequestTypeDef",
    {
        "AwsAccountId": str,
    },
)

DescribeAnalysisDefinitionRequestRequestTypeDef = TypedDict(
    "DescribeAnalysisDefinitionRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "AnalysisId": str,
    },
)

DescribeAnalysisPermissionsRequestRequestTypeDef = TypedDict(
    "DescribeAnalysisPermissionsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "AnalysisId": str,
    },
)

DescribeAnalysisRequestRequestTypeDef = TypedDict(
    "DescribeAnalysisRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "AnalysisId": str,
    },
)

_RequiredDescribeDashboardDefinitionRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeDashboardDefinitionRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DashboardId": str,
    },
)
_OptionalDescribeDashboardDefinitionRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeDashboardDefinitionRequestRequestTypeDef",
    {
        "VersionNumber": int,
        "AliasName": str,
    },
    total=False,
)


class DescribeDashboardDefinitionRequestRequestTypeDef(
    _RequiredDescribeDashboardDefinitionRequestRequestTypeDef,
    _OptionalDescribeDashboardDefinitionRequestRequestTypeDef,
):
    pass


DescribeDashboardPermissionsRequestRequestTypeDef = TypedDict(
    "DescribeDashboardPermissionsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DashboardId": str,
    },
)

_RequiredDescribeDashboardRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeDashboardRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DashboardId": str,
    },
)
_OptionalDescribeDashboardRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeDashboardRequestRequestTypeDef",
    {
        "VersionNumber": int,
        "AliasName": str,
    },
    total=False,
)


class DescribeDashboardRequestRequestTypeDef(
    _RequiredDescribeDashboardRequestRequestTypeDef, _OptionalDescribeDashboardRequestRequestTypeDef
):
    pass


DescribeDataSetPermissionsRequestRequestTypeDef = TypedDict(
    "DescribeDataSetPermissionsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DataSetId": str,
    },
)

DescribeDataSetRefreshPropertiesRequestRequestTypeDef = TypedDict(
    "DescribeDataSetRefreshPropertiesRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DataSetId": str,
    },
)

DescribeDataSetRequestRequestTypeDef = TypedDict(
    "DescribeDataSetRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DataSetId": str,
    },
)

DescribeDataSourcePermissionsRequestRequestTypeDef = TypedDict(
    "DescribeDataSourcePermissionsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DataSourceId": str,
    },
)

DescribeDataSourceRequestRequestTypeDef = TypedDict(
    "DescribeDataSourceRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DataSourceId": str,
    },
)

DescribeFolderPermissionsRequestRequestTypeDef = TypedDict(
    "DescribeFolderPermissionsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "FolderId": str,
    },
)

DescribeFolderRequestRequestTypeDef = TypedDict(
    "DescribeFolderRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "FolderId": str,
    },
)

DescribeFolderResolvedPermissionsRequestRequestTypeDef = TypedDict(
    "DescribeFolderResolvedPermissionsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "FolderId": str,
    },
)

FolderTypeDef = TypedDict(
    "FolderTypeDef",
    {
        "FolderId": str,
        "Arn": str,
        "Name": str,
        "FolderType": Literal["SHARED"],
        "FolderPath": List[str],
        "CreatedTime": datetime,
        "LastUpdatedTime": datetime,
    },
    total=False,
)

DescribeGroupMembershipRequestRequestTypeDef = TypedDict(
    "DescribeGroupMembershipRequestRequestTypeDef",
    {
        "MemberName": str,
        "GroupName": str,
        "AwsAccountId": str,
        "Namespace": str,
    },
)

DescribeGroupRequestRequestTypeDef = TypedDict(
    "DescribeGroupRequestRequestTypeDef",
    {
        "GroupName": str,
        "AwsAccountId": str,
        "Namespace": str,
    },
)

DescribeIAMPolicyAssignmentRequestRequestTypeDef = TypedDict(
    "DescribeIAMPolicyAssignmentRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "AssignmentName": str,
        "Namespace": str,
    },
)

IAMPolicyAssignmentTypeDef = TypedDict(
    "IAMPolicyAssignmentTypeDef",
    {
        "AwsAccountId": str,
        "AssignmentId": str,
        "AssignmentName": str,
        "PolicyArn": str,
        "Identities": Dict[str, List[str]],
        "AssignmentStatus": AssignmentStatusType,
    },
    total=False,
)

DescribeIngestionRequestRequestTypeDef = TypedDict(
    "DescribeIngestionRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DataSetId": str,
        "IngestionId": str,
    },
)

DescribeIpRestrictionRequestRequestTypeDef = TypedDict(
    "DescribeIpRestrictionRequestRequestTypeDef",
    {
        "AwsAccountId": str,
    },
)

DescribeNamespaceRequestRequestTypeDef = TypedDict(
    "DescribeNamespaceRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "Namespace": str,
    },
)

DescribeRefreshScheduleRequestRequestTypeDef = TypedDict(
    "DescribeRefreshScheduleRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DataSetId": str,
        "ScheduleId": str,
    },
)

DescribeTemplateAliasRequestRequestTypeDef = TypedDict(
    "DescribeTemplateAliasRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "TemplateId": str,
        "AliasName": str,
    },
)

_RequiredDescribeTemplateDefinitionRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeTemplateDefinitionRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "TemplateId": str,
    },
)
_OptionalDescribeTemplateDefinitionRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeTemplateDefinitionRequestRequestTypeDef",
    {
        "VersionNumber": int,
        "AliasName": str,
    },
    total=False,
)


class DescribeTemplateDefinitionRequestRequestTypeDef(
    _RequiredDescribeTemplateDefinitionRequestRequestTypeDef,
    _OptionalDescribeTemplateDefinitionRequestRequestTypeDef,
):
    pass


DescribeTemplatePermissionsRequestRequestTypeDef = TypedDict(
    "DescribeTemplatePermissionsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "TemplateId": str,
    },
)

_RequiredDescribeTemplateRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeTemplateRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "TemplateId": str,
    },
)
_OptionalDescribeTemplateRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeTemplateRequestRequestTypeDef",
    {
        "VersionNumber": int,
        "AliasName": str,
    },
    total=False,
)


class DescribeTemplateRequestRequestTypeDef(
    _RequiredDescribeTemplateRequestRequestTypeDef, _OptionalDescribeTemplateRequestRequestTypeDef
):
    pass


DescribeThemeAliasRequestRequestTypeDef = TypedDict(
    "DescribeThemeAliasRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "ThemeId": str,
        "AliasName": str,
    },
)

DescribeThemePermissionsRequestRequestTypeDef = TypedDict(
    "DescribeThemePermissionsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "ThemeId": str,
    },
)

_RequiredDescribeThemeRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeThemeRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "ThemeId": str,
    },
)
_OptionalDescribeThemeRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeThemeRequestRequestTypeDef",
    {
        "VersionNumber": int,
        "AliasName": str,
    },
    total=False,
)


class DescribeThemeRequestRequestTypeDef(
    _RequiredDescribeThemeRequestRequestTypeDef, _OptionalDescribeThemeRequestRequestTypeDef
):
    pass


DescribeUserRequestRequestTypeDef = TypedDict(
    "DescribeUserRequestRequestTypeDef",
    {
        "UserName": str,
        "AwsAccountId": str,
        "Namespace": str,
    },
)

UserTypeDef = TypedDict(
    "UserTypeDef",
    {
        "Arn": str,
        "UserName": str,
        "Email": str,
        "Role": UserRoleType,
        "IdentityType": IdentityTypeType,
        "Active": bool,
        "PrincipalId": str,
        "CustomPermissionsName": str,
        "ExternalLoginFederationProviderType": str,
        "ExternalLoginFederationProviderUrl": str,
        "ExternalLoginId": str,
    },
    total=False,
)

DonutCenterOptionsTypeDef = TypedDict(
    "DonutCenterOptionsTypeDef",
    {
        "LabelVisibility": VisibilityType,
    },
    total=False,
)

ListControlSelectAllOptionsTypeDef = TypedDict(
    "ListControlSelectAllOptionsTypeDef",
    {
        "Visibility": VisibilityType,
    },
    total=False,
)

ErrorInfoTypeDef = TypedDict(
    "ErrorInfoTypeDef",
    {
        "Type": IngestionErrorTypeType,
        "Message": str,
    },
    total=False,
)

_RequiredExcludePeriodConfigurationTypeDef = TypedDict(
    "_RequiredExcludePeriodConfigurationTypeDef",
    {
        "Amount": int,
        "Granularity": TimeGranularityType,
    },
)
_OptionalExcludePeriodConfigurationTypeDef = TypedDict(
    "_OptionalExcludePeriodConfigurationTypeDef",
    {
        "Status": WidgetStatusType,
    },
    total=False,
)


class ExcludePeriodConfigurationTypeDef(
    _RequiredExcludePeriodConfigurationTypeDef, _OptionalExcludePeriodConfigurationTypeDef
):
    pass


FieldSortTypeDef = TypedDict(
    "FieldSortTypeDef",
    {
        "FieldId": str,
        "Direction": SortDirectionType,
    },
)

_RequiredFieldTooltipItemTypeDef = TypedDict(
    "_RequiredFieldTooltipItemTypeDef",
    {
        "FieldId": str,
    },
)
_OptionalFieldTooltipItemTypeDef = TypedDict(
    "_OptionalFieldTooltipItemTypeDef",
    {
        "Label": str,
        "Visibility": VisibilityType,
    },
    total=False,
)


class FieldTooltipItemTypeDef(_RequiredFieldTooltipItemTypeDef, _OptionalFieldTooltipItemTypeDef):
    pass


GeospatialMapStyleOptionsTypeDef = TypedDict(
    "GeospatialMapStyleOptionsTypeDef",
    {
        "BaseMapStyle": BaseMapStyleTypeType,
    },
    total=False,
)

FilterSelectableValuesTypeDef = TypedDict(
    "FilterSelectableValuesTypeDef",
    {
        "Values": Sequence[str],
    },
    total=False,
)

SameSheetTargetVisualConfigurationTypeDef = TypedDict(
    "SameSheetTargetVisualConfigurationTypeDef",
    {
        "TargetVisuals": Sequence[str],
        "TargetVisualOptions": Literal["ALL_VISUALS"],
    },
    total=False,
)

FilterOperationTypeDef = TypedDict(
    "FilterOperationTypeDef",
    {
        "ConditionExpression": str,
    },
)

FolderSearchFilterTypeDef = TypedDict(
    "FolderSearchFilterTypeDef",
    {
        "Operator": FilterOperatorType,
        "Name": FolderFilterAttributeType,
        "Value": str,
    },
    total=False,
)

FolderSummaryTypeDef = TypedDict(
    "FolderSummaryTypeDef",
    {
        "Arn": str,
        "FolderId": str,
        "Name": str,
        "FolderType": Literal["SHARED"],
        "CreatedTime": datetime,
        "LastUpdatedTime": datetime,
    },
    total=False,
)

FontSizeTypeDef = TypedDict(
    "FontSizeTypeDef",
    {
        "Relative": RelativeFontSizeType,
    },
    total=False,
)

FontWeightTypeDef = TypedDict(
    "FontWeightTypeDef",
    {
        "Name": FontWeightNameType,
    },
    total=False,
)

FontTypeDef = TypedDict(
    "FontTypeDef",
    {
        "FontFamily": str,
    },
    total=False,
)

TimeBasedForecastPropertiesTypeDef = TypedDict(
    "TimeBasedForecastPropertiesTypeDef",
    {
        "PeriodsForward": int,
        "PeriodsBackward": int,
        "UpperBoundary": float,
        "LowerBoundary": float,
        "PredictionInterval": int,
        "Seasonality": int,
    },
    total=False,
)

WhatIfPointScenarioTypeDef = TypedDict(
    "WhatIfPointScenarioTypeDef",
    {
        "Date": Union[datetime, str],
        "Value": float,
    },
)

WhatIfRangeScenarioTypeDef = TypedDict(
    "WhatIfRangeScenarioTypeDef",
    {
        "StartDate": Union[datetime, str],
        "EndDate": Union[datetime, str],
        "Value": float,
    },
)

FreeFormLayoutScreenCanvasSizeOptionsTypeDef = TypedDict(
    "FreeFormLayoutScreenCanvasSizeOptionsTypeDef",
    {
        "OptimizedViewPortWidth": str,
    },
)

FreeFormLayoutElementBackgroundStyleTypeDef = TypedDict(
    "FreeFormLayoutElementBackgroundStyleTypeDef",
    {
        "Visibility": VisibilityType,
        "Color": str,
    },
    total=False,
)

FreeFormLayoutElementBorderStyleTypeDef = TypedDict(
    "FreeFormLayoutElementBorderStyleTypeDef",
    {
        "Visibility": VisibilityType,
        "Color": str,
    },
    total=False,
)

LoadingAnimationTypeDef = TypedDict(
    "LoadingAnimationTypeDef",
    {
        "Visibility": VisibilityType,
    },
    total=False,
)

SessionTagTypeDef = TypedDict(
    "SessionTagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

GeospatialCoordinateBoundsTypeDef = TypedDict(
    "GeospatialCoordinateBoundsTypeDef",
    {
        "North": float,
        "South": float,
        "West": float,
        "East": float,
    },
)

_RequiredGetDashboardEmbedUrlRequestRequestTypeDef = TypedDict(
    "_RequiredGetDashboardEmbedUrlRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DashboardId": str,
        "IdentityType": EmbeddingIdentityTypeType,
    },
)
_OptionalGetDashboardEmbedUrlRequestRequestTypeDef = TypedDict(
    "_OptionalGetDashboardEmbedUrlRequestRequestTypeDef",
    {
        "SessionLifetimeInMinutes": int,
        "UndoRedoDisabled": bool,
        "ResetDisabled": bool,
        "StatePersistenceEnabled": bool,
        "UserArn": str,
        "Namespace": str,
        "AdditionalDashboardIds": Sequence[str],
    },
    total=False,
)


class GetDashboardEmbedUrlRequestRequestTypeDef(
    _RequiredGetDashboardEmbedUrlRequestRequestTypeDef,
    _OptionalGetDashboardEmbedUrlRequestRequestTypeDef,
):
    pass


_RequiredGetSessionEmbedUrlRequestRequestTypeDef = TypedDict(
    "_RequiredGetSessionEmbedUrlRequestRequestTypeDef",
    {
        "AwsAccountId": str,
    },
)
_OptionalGetSessionEmbedUrlRequestRequestTypeDef = TypedDict(
    "_OptionalGetSessionEmbedUrlRequestRequestTypeDef",
    {
        "EntryPoint": str,
        "SessionLifetimeInMinutes": int,
        "UserArn": str,
    },
    total=False,
)


class GetSessionEmbedUrlRequestRequestTypeDef(
    _RequiredGetSessionEmbedUrlRequestRequestTypeDef,
    _OptionalGetSessionEmbedUrlRequestRequestTypeDef,
):
    pass


TableBorderOptionsTypeDef = TypedDict(
    "TableBorderOptionsTypeDef",
    {
        "Color": str,
        "Thickness": int,
        "Style": TableBorderStyleType,
    },
    total=False,
)

_RequiredGradientStopTypeDef = TypedDict(
    "_RequiredGradientStopTypeDef",
    {
        "GradientOffset": float,
    },
)
_OptionalGradientStopTypeDef = TypedDict(
    "_OptionalGradientStopTypeDef",
    {
        "DataValue": float,
        "Color": str,
    },
    total=False,
)


class GradientStopTypeDef(_RequiredGradientStopTypeDef, _OptionalGradientStopTypeDef):
    pass


_RequiredGridLayoutScreenCanvasSizeOptionsTypeDef = TypedDict(
    "_RequiredGridLayoutScreenCanvasSizeOptionsTypeDef",
    {
        "ResizeOption": ResizeOptionType,
    },
)
_OptionalGridLayoutScreenCanvasSizeOptionsTypeDef = TypedDict(
    "_OptionalGridLayoutScreenCanvasSizeOptionsTypeDef",
    {
        "OptimizedViewPortWidth": str,
    },
    total=False,
)


class GridLayoutScreenCanvasSizeOptionsTypeDef(
    _RequiredGridLayoutScreenCanvasSizeOptionsTypeDef,
    _OptionalGridLayoutScreenCanvasSizeOptionsTypeDef,
):
    pass


_RequiredGridLayoutElementTypeDef = TypedDict(
    "_RequiredGridLayoutElementTypeDef",
    {
        "ElementId": str,
        "ElementType": LayoutElementTypeType,
        "ColumnSpan": int,
        "RowSpan": int,
    },
)
_OptionalGridLayoutElementTypeDef = TypedDict(
    "_OptionalGridLayoutElementTypeDef",
    {
        "ColumnIndex": int,
        "RowIndex": int,
    },
    total=False,
)


class GridLayoutElementTypeDef(
    _RequiredGridLayoutElementTypeDef, _OptionalGridLayoutElementTypeDef
):
    pass


GroupSearchFilterTypeDef = TypedDict(
    "GroupSearchFilterTypeDef",
    {
        "Operator": Literal["StartsWith"],
        "Name": Literal["GROUP_NAME"],
        "Value": str,
    },
)

GutterStyleTypeDef = TypedDict(
    "GutterStyleTypeDef",
    {
        "Show": bool,
    },
    total=False,
)

IAMPolicyAssignmentSummaryTypeDef = TypedDict(
    "IAMPolicyAssignmentSummaryTypeDef",
    {
        "AssignmentName": str,
        "AssignmentStatus": AssignmentStatusType,
    },
    total=False,
)

LookbackWindowTypeDef = TypedDict(
    "LookbackWindowTypeDef",
    {
        "ColumnName": str,
        "Size": int,
        "SizeUnit": LookbackWindowSizeUnitType,
    },
)

QueueInfoTypeDef = TypedDict(
    "QueueInfoTypeDef",
    {
        "WaitingOnIngestion": str,
        "QueuedIngestion": str,
    },
)

RowInfoTypeDef = TypedDict(
    "RowInfoTypeDef",
    {
        "RowsIngested": int,
        "RowsDropped": int,
        "TotalRowsInDataset": int,
    },
    total=False,
)

IntegerValueWhenUnsetConfigurationTypeDef = TypedDict(
    "IntegerValueWhenUnsetConfigurationTypeDef",
    {
        "ValueWhenUnsetOption": ValueWhenUnsetOptionType,
        "CustomValue": int,
    },
    total=False,
)

IntegerParameterTypeDef = TypedDict(
    "IntegerParameterTypeDef",
    {
        "Name": str,
        "Values": Sequence[int],
    },
)

JoinKeyPropertiesTypeDef = TypedDict(
    "JoinKeyPropertiesTypeDef",
    {
        "UniqueKey": bool,
    },
    total=False,
)

ProgressBarOptionsTypeDef = TypedDict(
    "ProgressBarOptionsTypeDef",
    {
        "Visibility": VisibilityType,
    },
    total=False,
)

SecondaryValueOptionsTypeDef = TypedDict(
    "SecondaryValueOptionsTypeDef",
    {
        "Visibility": VisibilityType,
    },
    total=False,
)

TrendArrowOptionsTypeDef = TypedDict(
    "TrendArrowOptionsTypeDef",
    {
        "Visibility": VisibilityType,
    },
    total=False,
)

LineChartLineStyleSettingsTypeDef = TypedDict(
    "LineChartLineStyleSettingsTypeDef",
    {
        "LineVisibility": VisibilityType,
        "LineInterpolation": LineInterpolationType,
        "LineStyle": LineChartLineStyleType,
        "LineWidth": str,
    },
    total=False,
)

LineChartMarkerStyleSettingsTypeDef = TypedDict(
    "LineChartMarkerStyleSettingsTypeDef",
    {
        "MarkerVisibility": VisibilityType,
        "MarkerShape": LineChartMarkerShapeType,
        "MarkerSize": str,
        "MarkerColor": str,
    },
    total=False,
)

MissingDataConfigurationTypeDef = TypedDict(
    "MissingDataConfigurationTypeDef",
    {
        "TreatmentOption": MissingDataTreatmentOptionType,
    },
    total=False,
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": int,
        "PageSize": int,
        "StartingToken": str,
    },
    total=False,
)

_RequiredListAnalysesRequestRequestTypeDef = TypedDict(
    "_RequiredListAnalysesRequestRequestTypeDef",
    {
        "AwsAccountId": str,
    },
)
_OptionalListAnalysesRequestRequestTypeDef = TypedDict(
    "_OptionalListAnalysesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListAnalysesRequestRequestTypeDef(
    _RequiredListAnalysesRequestRequestTypeDef, _OptionalListAnalysesRequestRequestTypeDef
):
    pass


ListControlSearchOptionsTypeDef = TypedDict(
    "ListControlSearchOptionsTypeDef",
    {
        "Visibility": VisibilityType,
    },
    total=False,
)

_RequiredListDashboardVersionsRequestRequestTypeDef = TypedDict(
    "_RequiredListDashboardVersionsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DashboardId": str,
    },
)
_OptionalListDashboardVersionsRequestRequestTypeDef = TypedDict(
    "_OptionalListDashboardVersionsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListDashboardVersionsRequestRequestTypeDef(
    _RequiredListDashboardVersionsRequestRequestTypeDef,
    _OptionalListDashboardVersionsRequestRequestTypeDef,
):
    pass


_RequiredListDashboardsRequestRequestTypeDef = TypedDict(
    "_RequiredListDashboardsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
    },
)
_OptionalListDashboardsRequestRequestTypeDef = TypedDict(
    "_OptionalListDashboardsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListDashboardsRequestRequestTypeDef(
    _RequiredListDashboardsRequestRequestTypeDef, _OptionalListDashboardsRequestRequestTypeDef
):
    pass


_RequiredListDataSetsRequestRequestTypeDef = TypedDict(
    "_RequiredListDataSetsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
    },
)
_OptionalListDataSetsRequestRequestTypeDef = TypedDict(
    "_OptionalListDataSetsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListDataSetsRequestRequestTypeDef(
    _RequiredListDataSetsRequestRequestTypeDef, _OptionalListDataSetsRequestRequestTypeDef
):
    pass


_RequiredListDataSourcesRequestRequestTypeDef = TypedDict(
    "_RequiredListDataSourcesRequestRequestTypeDef",
    {
        "AwsAccountId": str,
    },
)
_OptionalListDataSourcesRequestRequestTypeDef = TypedDict(
    "_OptionalListDataSourcesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListDataSourcesRequestRequestTypeDef(
    _RequiredListDataSourcesRequestRequestTypeDef, _OptionalListDataSourcesRequestRequestTypeDef
):
    pass


_RequiredListFolderMembersRequestRequestTypeDef = TypedDict(
    "_RequiredListFolderMembersRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "FolderId": str,
    },
)
_OptionalListFolderMembersRequestRequestTypeDef = TypedDict(
    "_OptionalListFolderMembersRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListFolderMembersRequestRequestTypeDef(
    _RequiredListFolderMembersRequestRequestTypeDef, _OptionalListFolderMembersRequestRequestTypeDef
):
    pass


MemberIdArnPairTypeDef = TypedDict(
    "MemberIdArnPairTypeDef",
    {
        "MemberId": str,
        "MemberArn": str,
    },
    total=False,
)

_RequiredListFoldersRequestRequestTypeDef = TypedDict(
    "_RequiredListFoldersRequestRequestTypeDef",
    {
        "AwsAccountId": str,
    },
)
_OptionalListFoldersRequestRequestTypeDef = TypedDict(
    "_OptionalListFoldersRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListFoldersRequestRequestTypeDef(
    _RequiredListFoldersRequestRequestTypeDef, _OptionalListFoldersRequestRequestTypeDef
):
    pass


_RequiredListGroupMembershipsRequestRequestTypeDef = TypedDict(
    "_RequiredListGroupMembershipsRequestRequestTypeDef",
    {
        "GroupName": str,
        "AwsAccountId": str,
        "Namespace": str,
    },
)
_OptionalListGroupMembershipsRequestRequestTypeDef = TypedDict(
    "_OptionalListGroupMembershipsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListGroupMembershipsRequestRequestTypeDef(
    _RequiredListGroupMembershipsRequestRequestTypeDef,
    _OptionalListGroupMembershipsRequestRequestTypeDef,
):
    pass


_RequiredListGroupsRequestRequestTypeDef = TypedDict(
    "_RequiredListGroupsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "Namespace": str,
    },
)
_OptionalListGroupsRequestRequestTypeDef = TypedDict(
    "_OptionalListGroupsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListGroupsRequestRequestTypeDef(
    _RequiredListGroupsRequestRequestTypeDef, _OptionalListGroupsRequestRequestTypeDef
):
    pass


_RequiredListIAMPolicyAssignmentsForUserRequestRequestTypeDef = TypedDict(
    "_RequiredListIAMPolicyAssignmentsForUserRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "UserName": str,
        "Namespace": str,
    },
)
_OptionalListIAMPolicyAssignmentsForUserRequestRequestTypeDef = TypedDict(
    "_OptionalListIAMPolicyAssignmentsForUserRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListIAMPolicyAssignmentsForUserRequestRequestTypeDef(
    _RequiredListIAMPolicyAssignmentsForUserRequestRequestTypeDef,
    _OptionalListIAMPolicyAssignmentsForUserRequestRequestTypeDef,
):
    pass


_RequiredListIAMPolicyAssignmentsRequestRequestTypeDef = TypedDict(
    "_RequiredListIAMPolicyAssignmentsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "Namespace": str,
    },
)
_OptionalListIAMPolicyAssignmentsRequestRequestTypeDef = TypedDict(
    "_OptionalListIAMPolicyAssignmentsRequestRequestTypeDef",
    {
        "AssignmentStatus": AssignmentStatusType,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListIAMPolicyAssignmentsRequestRequestTypeDef(
    _RequiredListIAMPolicyAssignmentsRequestRequestTypeDef,
    _OptionalListIAMPolicyAssignmentsRequestRequestTypeDef,
):
    pass


_RequiredListIngestionsRequestRequestTypeDef = TypedDict(
    "_RequiredListIngestionsRequestRequestTypeDef",
    {
        "DataSetId": str,
        "AwsAccountId": str,
    },
)
_OptionalListIngestionsRequestRequestTypeDef = TypedDict(
    "_OptionalListIngestionsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListIngestionsRequestRequestTypeDef(
    _RequiredListIngestionsRequestRequestTypeDef, _OptionalListIngestionsRequestRequestTypeDef
):
    pass


_RequiredListNamespacesRequestRequestTypeDef = TypedDict(
    "_RequiredListNamespacesRequestRequestTypeDef",
    {
        "AwsAccountId": str,
    },
)
_OptionalListNamespacesRequestRequestTypeDef = TypedDict(
    "_OptionalListNamespacesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListNamespacesRequestRequestTypeDef(
    _RequiredListNamespacesRequestRequestTypeDef, _OptionalListNamespacesRequestRequestTypeDef
):
    pass


ListRefreshSchedulesRequestRequestTypeDef = TypedDict(
    "ListRefreshSchedulesRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DataSetId": str,
    },
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

_RequiredListTemplateAliasesRequestRequestTypeDef = TypedDict(
    "_RequiredListTemplateAliasesRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "TemplateId": str,
    },
)
_OptionalListTemplateAliasesRequestRequestTypeDef = TypedDict(
    "_OptionalListTemplateAliasesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListTemplateAliasesRequestRequestTypeDef(
    _RequiredListTemplateAliasesRequestRequestTypeDef,
    _OptionalListTemplateAliasesRequestRequestTypeDef,
):
    pass


_RequiredListTemplateVersionsRequestRequestTypeDef = TypedDict(
    "_RequiredListTemplateVersionsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "TemplateId": str,
    },
)
_OptionalListTemplateVersionsRequestRequestTypeDef = TypedDict(
    "_OptionalListTemplateVersionsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListTemplateVersionsRequestRequestTypeDef(
    _RequiredListTemplateVersionsRequestRequestTypeDef,
    _OptionalListTemplateVersionsRequestRequestTypeDef,
):
    pass


TemplateVersionSummaryTypeDef = TypedDict(
    "TemplateVersionSummaryTypeDef",
    {
        "Arn": str,
        "VersionNumber": int,
        "CreatedTime": datetime,
        "Status": ResourceStatusType,
        "Description": str,
    },
    total=False,
)

_RequiredListTemplatesRequestRequestTypeDef = TypedDict(
    "_RequiredListTemplatesRequestRequestTypeDef",
    {
        "AwsAccountId": str,
    },
)
_OptionalListTemplatesRequestRequestTypeDef = TypedDict(
    "_OptionalListTemplatesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListTemplatesRequestRequestTypeDef(
    _RequiredListTemplatesRequestRequestTypeDef, _OptionalListTemplatesRequestRequestTypeDef
):
    pass


TemplateSummaryTypeDef = TypedDict(
    "TemplateSummaryTypeDef",
    {
        "Arn": str,
        "TemplateId": str,
        "Name": str,
        "LatestVersionNumber": int,
        "CreatedTime": datetime,
        "LastUpdatedTime": datetime,
    },
    total=False,
)

_RequiredListThemeAliasesRequestRequestTypeDef = TypedDict(
    "_RequiredListThemeAliasesRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "ThemeId": str,
    },
)
_OptionalListThemeAliasesRequestRequestTypeDef = TypedDict(
    "_OptionalListThemeAliasesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListThemeAliasesRequestRequestTypeDef(
    _RequiredListThemeAliasesRequestRequestTypeDef, _OptionalListThemeAliasesRequestRequestTypeDef
):
    pass


_RequiredListThemeVersionsRequestRequestTypeDef = TypedDict(
    "_RequiredListThemeVersionsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "ThemeId": str,
    },
)
_OptionalListThemeVersionsRequestRequestTypeDef = TypedDict(
    "_OptionalListThemeVersionsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListThemeVersionsRequestRequestTypeDef(
    _RequiredListThemeVersionsRequestRequestTypeDef, _OptionalListThemeVersionsRequestRequestTypeDef
):
    pass


ThemeVersionSummaryTypeDef = TypedDict(
    "ThemeVersionSummaryTypeDef",
    {
        "VersionNumber": int,
        "Arn": str,
        "Description": str,
        "CreatedTime": datetime,
        "Status": ResourceStatusType,
    },
    total=False,
)

_RequiredListThemesRequestRequestTypeDef = TypedDict(
    "_RequiredListThemesRequestRequestTypeDef",
    {
        "AwsAccountId": str,
    },
)
_OptionalListThemesRequestRequestTypeDef = TypedDict(
    "_OptionalListThemesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "Type": ThemeTypeType,
    },
    total=False,
)


class ListThemesRequestRequestTypeDef(
    _RequiredListThemesRequestRequestTypeDef, _OptionalListThemesRequestRequestTypeDef
):
    pass


ThemeSummaryTypeDef = TypedDict(
    "ThemeSummaryTypeDef",
    {
        "Arn": str,
        "Name": str,
        "ThemeId": str,
        "LatestVersionNumber": int,
        "CreatedTime": datetime,
        "LastUpdatedTime": datetime,
    },
    total=False,
)

_RequiredListUserGroupsRequestRequestTypeDef = TypedDict(
    "_RequiredListUserGroupsRequestRequestTypeDef",
    {
        "UserName": str,
        "AwsAccountId": str,
        "Namespace": str,
    },
)
_OptionalListUserGroupsRequestRequestTypeDef = TypedDict(
    "_OptionalListUserGroupsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListUserGroupsRequestRequestTypeDef(
    _RequiredListUserGroupsRequestRequestTypeDef, _OptionalListUserGroupsRequestRequestTypeDef
):
    pass


_RequiredListUsersRequestRequestTypeDef = TypedDict(
    "_RequiredListUsersRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "Namespace": str,
    },
)
_OptionalListUsersRequestRequestTypeDef = TypedDict(
    "_OptionalListUsersRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListUsersRequestRequestTypeDef(
    _RequiredListUsersRequestRequestTypeDef, _OptionalListUsersRequestRequestTypeDef
):
    pass


LongFormatTextTypeDef = TypedDict(
    "LongFormatTextTypeDef",
    {
        "PlainText": str,
        "RichText": str,
    },
    total=False,
)

ManifestFileLocationTypeDef = TypedDict(
    "ManifestFileLocationTypeDef",
    {
        "Bucket": str,
        "Key": str,
    },
)

MarginStyleTypeDef = TypedDict(
    "MarginStyleTypeDef",
    {
        "Show": bool,
    },
    total=False,
)

NamespaceErrorTypeDef = TypedDict(
    "NamespaceErrorTypeDef",
    {
        "Type": NamespaceErrorTypeType,
        "Message": str,
    },
    total=False,
)

NumericRangeFilterValueTypeDef = TypedDict(
    "NumericRangeFilterValueTypeDef",
    {
        "StaticValue": float,
        "Parameter": str,
    },
    total=False,
)

ThousandSeparatorOptionsTypeDef = TypedDict(
    "ThousandSeparatorOptionsTypeDef",
    {
        "Symbol": NumericSeparatorSymbolType,
        "Visibility": VisibilityType,
    },
    total=False,
)

PercentileAggregationTypeDef = TypedDict(
    "PercentileAggregationTypeDef",
    {
        "PercentileValue": float,
    },
    total=False,
)

StringParameterTypeDef = TypedDict(
    "StringParameterTypeDef",
    {
        "Name": str,
        "Values": Sequence[str],
    },
)

PercentVisibleRangeTypeDef = TypedDict(
    "PercentVisibleRangeTypeDef",
    {
        "From": float,
        "To": float,
    },
    total=False,
)

PivotTableConditionalFormattingScopeTypeDef = TypedDict(
    "PivotTableConditionalFormattingScopeTypeDef",
    {
        "Role": PivotTableConditionalFormattingScopeRoleType,
    },
    total=False,
)

PivotTablePaginatedReportOptionsTypeDef = TypedDict(
    "PivotTablePaginatedReportOptionsTypeDef",
    {
        "VerticalOverflowVisibility": VisibilityType,
        "OverflowColumnHeaderVisibility": VisibilityType,
    },
    total=False,
)

_RequiredPivotTableFieldOptionTypeDef = TypedDict(
    "_RequiredPivotTableFieldOptionTypeDef",
    {
        "FieldId": str,
    },
)
_OptionalPivotTableFieldOptionTypeDef = TypedDict(
    "_OptionalPivotTableFieldOptionTypeDef",
    {
        "CustomLabel": str,
        "Visibility": VisibilityType,
    },
    total=False,
)


class PivotTableFieldOptionTypeDef(
    _RequiredPivotTableFieldOptionTypeDef, _OptionalPivotTableFieldOptionTypeDef
):
    pass


PivotTableFieldSubtotalOptionsTypeDef = TypedDict(
    "PivotTableFieldSubtotalOptionsTypeDef",
    {
        "FieldId": str,
    },
    total=False,
)

RowAlternateColorOptionsTypeDef = TypedDict(
    "RowAlternateColorOptionsTypeDef",
    {
        "Status": WidgetStatusType,
        "RowAlternateColors": Sequence[str],
    },
    total=False,
)

ProjectOperationTypeDef = TypedDict(
    "ProjectOperationTypeDef",
    {
        "ProjectedColumns": Sequence[str],
    },
)

RadarChartAreaStyleSettingsTypeDef = TypedDict(
    "RadarChartAreaStyleSettingsTypeDef",
    {
        "Visibility": VisibilityType,
    },
    total=False,
)

ReferenceLineCustomLabelConfigurationTypeDef = TypedDict(
    "ReferenceLineCustomLabelConfigurationTypeDef",
    {
        "CustomLabel": str,
    },
)

ReferenceLineStaticDataConfigurationTypeDef = TypedDict(
    "ReferenceLineStaticDataConfigurationTypeDef",
    {
        "Value": float,
    },
)

ReferenceLineStyleConfigurationTypeDef = TypedDict(
    "ReferenceLineStyleConfigurationTypeDef",
    {
        "Pattern": ReferenceLinePatternTypeType,
        "Color": str,
    },
    total=False,
)

ScheduleRefreshOnEntityTypeDef = TypedDict(
    "ScheduleRefreshOnEntityTypeDef",
    {
        "DayOfWeek": DayOfWeekType,
        "DayOfMonth": str,
    },
    total=False,
)

_RequiredRegisterUserRequestRequestTypeDef = TypedDict(
    "_RequiredRegisterUserRequestRequestTypeDef",
    {
        "IdentityType": IdentityTypeType,
        "Email": str,
        "UserRole": UserRoleType,
        "AwsAccountId": str,
        "Namespace": str,
    },
)
_OptionalRegisterUserRequestRequestTypeDef = TypedDict(
    "_OptionalRegisterUserRequestRequestTypeDef",
    {
        "IamArn": str,
        "SessionName": str,
        "UserName": str,
        "CustomPermissionsName": str,
        "ExternalLoginFederationProviderType": str,
        "CustomFederationProviderUrl": str,
        "ExternalLoginId": str,
    },
    total=False,
)


class RegisterUserRequestRequestTypeDef(
    _RequiredRegisterUserRequestRequestTypeDef, _OptionalRegisterUserRequestRequestTypeDef
):
    pass


StatePersistenceConfigurationsTypeDef = TypedDict(
    "StatePersistenceConfigurationsTypeDef",
    {
        "Enabled": bool,
    },
)

RegisteredUserQSearchBarEmbeddingConfigurationTypeDef = TypedDict(
    "RegisteredUserQSearchBarEmbeddingConfigurationTypeDef",
    {
        "InitialTopicId": str,
    },
    total=False,
)

RenameColumnOperationTypeDef = TypedDict(
    "RenameColumnOperationTypeDef",
    {
        "ColumnName": str,
        "NewColumnName": str,
    },
)

RestoreAnalysisRequestRequestTypeDef = TypedDict(
    "RestoreAnalysisRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "AnalysisId": str,
    },
)

_RequiredRowLevelPermissionTagRuleTypeDef = TypedDict(
    "_RequiredRowLevelPermissionTagRuleTypeDef",
    {
        "TagKey": str,
        "ColumnName": str,
    },
)
_OptionalRowLevelPermissionTagRuleTypeDef = TypedDict(
    "_OptionalRowLevelPermissionTagRuleTypeDef",
    {
        "TagMultiValueDelimiter": str,
        "MatchAllValue": str,
    },
    total=False,
)


class RowLevelPermissionTagRuleTypeDef(
    _RequiredRowLevelPermissionTagRuleTypeDef, _OptionalRowLevelPermissionTagRuleTypeDef
):
    pass


UploadSettingsTypeDef = TypedDict(
    "UploadSettingsTypeDef",
    {
        "Format": FileFormatType,
        "StartFromRow": int,
        "ContainsHeader": bool,
        "TextQualifier": TextQualifierType,
        "Delimiter": str,
    },
    total=False,
)

SectionAfterPageBreakTypeDef = TypedDict(
    "SectionAfterPageBreakTypeDef",
    {
        "Status": SectionPageBreakStatusType,
    },
    total=False,
)

SpacingTypeDef = TypedDict(
    "SpacingTypeDef",
    {
        "Top": str,
        "Bottom": str,
        "Left": str,
        "Right": str,
    },
    total=False,
)

_RequiredSheetVisualScopingConfigurationTypeDef = TypedDict(
    "_RequiredSheetVisualScopingConfigurationTypeDef",
    {
        "SheetId": str,
        "Scope": FilterVisualScopeType,
    },
)
_OptionalSheetVisualScopingConfigurationTypeDef = TypedDict(
    "_OptionalSheetVisualScopingConfigurationTypeDef",
    {
        "VisualIds": Sequence[str],
    },
    total=False,
)


class SheetVisualScopingConfigurationTypeDef(
    _RequiredSheetVisualScopingConfigurationTypeDef, _OptionalSheetVisualScopingConfigurationTypeDef
):
    pass


_RequiredSheetTextBoxTypeDef = TypedDict(
    "_RequiredSheetTextBoxTypeDef",
    {
        "SheetTextBoxId": str,
    },
)
_OptionalSheetTextBoxTypeDef = TypedDict(
    "_OptionalSheetTextBoxTypeDef",
    {
        "Content": str,
    },
    total=False,
)


class SheetTextBoxTypeDef(_RequiredSheetTextBoxTypeDef, _OptionalSheetTextBoxTypeDef):
    pass


SheetElementConfigurationOverridesTypeDef = TypedDict(
    "SheetElementConfigurationOverridesTypeDef",
    {
        "Visibility": VisibilityType,
    },
    total=False,
)

ShortFormatTextTypeDef = TypedDict(
    "ShortFormatTextTypeDef",
    {
        "PlainText": str,
        "RichText": str,
    },
    total=False,
)

StringValueWhenUnsetConfigurationTypeDef = TypedDict(
    "StringValueWhenUnsetConfigurationTypeDef",
    {
        "ValueWhenUnsetOption": ValueWhenUnsetOptionType,
        "CustomValue": str,
    },
    total=False,
)

TableCellImageSizingConfigurationTypeDef = TypedDict(
    "TableCellImageSizingConfigurationTypeDef",
    {
        "TableCellImageScalingConfiguration": TableCellImageScalingConfigurationType,
    },
    total=False,
)

TablePaginatedReportOptionsTypeDef = TypedDict(
    "TablePaginatedReportOptionsTypeDef",
    {
        "VerticalOverflowVisibility": VisibilityType,
        "OverflowColumnHeaderVisibility": VisibilityType,
    },
    total=False,
)

TableFieldCustomIconContentTypeDef = TypedDict(
    "TableFieldCustomIconContentTypeDef",
    {
        "Icon": Literal["LINK"],
    },
    total=False,
)

TemplateSourceTemplateTypeDef = TypedDict(
    "TemplateSourceTemplateTypeDef",
    {
        "Arn": str,
    },
)

TextControlPlaceholderOptionsTypeDef = TypedDict(
    "TextControlPlaceholderOptionsTypeDef",
    {
        "Visibility": VisibilityType,
    },
    total=False,
)

UIColorPaletteTypeDef = TypedDict(
    "UIColorPaletteTypeDef",
    {
        "PrimaryForeground": str,
        "PrimaryBackground": str,
        "SecondaryForeground": str,
        "SecondaryBackground": str,
        "Accent": str,
        "AccentForeground": str,
        "Danger": str,
        "DangerForeground": str,
        "Warning": str,
        "WarningForeground": str,
        "Success": str,
        "SuccessForeground": str,
        "Dimension": str,
        "DimensionForeground": str,
        "Measure": str,
        "MeasureForeground": str,
    },
    total=False,
)

ThemeErrorTypeDef = TypedDict(
    "ThemeErrorTypeDef",
    {
        "Type": Literal["INTERNAL_FAILURE"],
        "Message": str,
    },
    total=False,
)

UntagColumnOperationTypeDef = TypedDict(
    "UntagColumnOperationTypeDef",
    {
        "ColumnName": str,
        "TagNames": Sequence[ColumnTagNameType],
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "TagKeys": Sequence[str],
    },
)

_RequiredUpdateAccountSettingsRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateAccountSettingsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DefaultNamespace": str,
    },
)
_OptionalUpdateAccountSettingsRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateAccountSettingsRequestRequestTypeDef",
    {
        "NotificationEmail": str,
        "TerminationProtectionEnabled": bool,
    },
    total=False,
)


class UpdateAccountSettingsRequestRequestTypeDef(
    _RequiredUpdateAccountSettingsRequestRequestTypeDef,
    _OptionalUpdateAccountSettingsRequestRequestTypeDef,
):
    pass


UpdateDashboardPublishedVersionRequestRequestTypeDef = TypedDict(
    "UpdateDashboardPublishedVersionRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DashboardId": str,
        "VersionNumber": int,
    },
)

UpdateFolderRequestRequestTypeDef = TypedDict(
    "UpdateFolderRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "FolderId": str,
        "Name": str,
    },
)

_RequiredUpdateGroupRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateGroupRequestRequestTypeDef",
    {
        "GroupName": str,
        "AwsAccountId": str,
        "Namespace": str,
    },
)
_OptionalUpdateGroupRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateGroupRequestRequestTypeDef",
    {
        "Description": str,
    },
    total=False,
)


class UpdateGroupRequestRequestTypeDef(
    _RequiredUpdateGroupRequestRequestTypeDef, _OptionalUpdateGroupRequestRequestTypeDef
):
    pass


_RequiredUpdateIAMPolicyAssignmentRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateIAMPolicyAssignmentRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "AssignmentName": str,
        "Namespace": str,
    },
)
_OptionalUpdateIAMPolicyAssignmentRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateIAMPolicyAssignmentRequestRequestTypeDef",
    {
        "AssignmentStatus": AssignmentStatusType,
        "PolicyArn": str,
        "Identities": Mapping[str, Sequence[str]],
    },
    total=False,
)


class UpdateIAMPolicyAssignmentRequestRequestTypeDef(
    _RequiredUpdateIAMPolicyAssignmentRequestRequestTypeDef,
    _OptionalUpdateIAMPolicyAssignmentRequestRequestTypeDef,
):
    pass


_RequiredUpdateIpRestrictionRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateIpRestrictionRequestRequestTypeDef",
    {
        "AwsAccountId": str,
    },
)
_OptionalUpdateIpRestrictionRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateIpRestrictionRequestRequestTypeDef",
    {
        "IpRestrictionRuleMap": Mapping[str, str],
        "Enabled": bool,
    },
    total=False,
)


class UpdateIpRestrictionRequestRequestTypeDef(
    _RequiredUpdateIpRestrictionRequestRequestTypeDef,
    _OptionalUpdateIpRestrictionRequestRequestTypeDef,
):
    pass


_RequiredUpdatePublicSharingSettingsRequestRequestTypeDef = TypedDict(
    "_RequiredUpdatePublicSharingSettingsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
    },
)
_OptionalUpdatePublicSharingSettingsRequestRequestTypeDef = TypedDict(
    "_OptionalUpdatePublicSharingSettingsRequestRequestTypeDef",
    {
        "PublicSharingEnabled": bool,
    },
    total=False,
)


class UpdatePublicSharingSettingsRequestRequestTypeDef(
    _RequiredUpdatePublicSharingSettingsRequestRequestTypeDef,
    _OptionalUpdatePublicSharingSettingsRequestRequestTypeDef,
):
    pass


UpdateTemplateAliasRequestRequestTypeDef = TypedDict(
    "UpdateTemplateAliasRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "TemplateId": str,
        "AliasName": str,
        "TemplateVersionNumber": int,
    },
)

UpdateThemeAliasRequestRequestTypeDef = TypedDict(
    "UpdateThemeAliasRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "ThemeId": str,
        "AliasName": str,
        "ThemeVersionNumber": int,
    },
)

_RequiredUpdateUserRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateUserRequestRequestTypeDef",
    {
        "UserName": str,
        "AwsAccountId": str,
        "Namespace": str,
        "Email": str,
        "Role": UserRoleType,
    },
)
_OptionalUpdateUserRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateUserRequestRequestTypeDef",
    {
        "CustomPermissionsName": str,
        "UnapplyCustomPermissions": bool,
        "ExternalLoginFederationProviderType": str,
        "CustomFederationProviderUrl": str,
        "ExternalLoginId": str,
    },
    total=False,
)


class UpdateUserRequestRequestTypeDef(
    _RequiredUpdateUserRequestRequestTypeDef, _OptionalUpdateUserRequestRequestTypeDef
):
    pass


WaterfallChartOptionsTypeDef = TypedDict(
    "WaterfallChartOptionsTypeDef",
    {
        "TotalBarLabel": str,
    },
    total=False,
)

WordCloudOptionsTypeDef = TypedDict(
    "WordCloudOptionsTypeDef",
    {
        "WordOrientation": WordCloudWordOrientationType,
        "WordScaling": WordCloudWordScalingType,
        "CloudLayout": WordCloudCloudLayoutType,
        "WordCasing": WordCloudWordCasingType,
        "WordPadding": WordCloudWordPaddingType,
        "MaximumStringLength": int,
    },
    total=False,
)

_RequiredUpdateAccountCustomizationRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateAccountCustomizationRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "AccountCustomization": AccountCustomizationTypeDef,
    },
)
_OptionalUpdateAccountCustomizationRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateAccountCustomizationRequestRequestTypeDef",
    {
        "Namespace": str,
    },
    total=False,
)


class UpdateAccountCustomizationRequestRequestTypeDef(
    _RequiredUpdateAccountCustomizationRequestRequestTypeDef,
    _OptionalUpdateAccountCustomizationRequestRequestTypeDef,
):
    pass


AxisLabelReferenceOptionsTypeDef = TypedDict(
    "AxisLabelReferenceOptionsTypeDef",
    {
        "FieldId": str,
        "Column": ColumnIdentifierTypeDef,
    },
)

CascadingControlSourceTypeDef = TypedDict(
    "CascadingControlSourceTypeDef",
    {
        "SourceSheetControlId": str,
        "ColumnToMatch": ColumnIdentifierTypeDef,
    },
    total=False,
)

CategoryDrillDownFilterTypeDef = TypedDict(
    "CategoryDrillDownFilterTypeDef",
    {
        "Column": ColumnIdentifierTypeDef,
        "CategoryValues": Sequence[str],
    },
)

ContributionAnalysisDefaultTypeDef = TypedDict(
    "ContributionAnalysisDefaultTypeDef",
    {
        "MeasureFieldId": str,
        "ContributorDimensions": Sequence[ColumnIdentifierTypeDef],
    },
)

_RequiredDynamicDefaultValueTypeDef = TypedDict(
    "_RequiredDynamicDefaultValueTypeDef",
    {
        "DefaultValueColumn": ColumnIdentifierTypeDef,
    },
)
_OptionalDynamicDefaultValueTypeDef = TypedDict(
    "_OptionalDynamicDefaultValueTypeDef",
    {
        "UserNameColumn": ColumnIdentifierTypeDef,
        "GroupNameColumn": ColumnIdentifierTypeDef,
    },
    total=False,
)


class DynamicDefaultValueTypeDef(
    _RequiredDynamicDefaultValueTypeDef, _OptionalDynamicDefaultValueTypeDef
):
    pass


NumericEqualityDrillDownFilterTypeDef = TypedDict(
    "NumericEqualityDrillDownFilterTypeDef",
    {
        "Column": ColumnIdentifierTypeDef,
        "Value": float,
    },
)

ParameterSelectableValuesTypeDef = TypedDict(
    "ParameterSelectableValuesTypeDef",
    {
        "Values": Sequence[str],
        "LinkToDataSetColumn": ColumnIdentifierTypeDef,
    },
    total=False,
)

_RequiredTimeEqualityFilterTypeDef = TypedDict(
    "_RequiredTimeEqualityFilterTypeDef",
    {
        "FilterId": str,
        "Column": ColumnIdentifierTypeDef,
    },
)
_OptionalTimeEqualityFilterTypeDef = TypedDict(
    "_OptionalTimeEqualityFilterTypeDef",
    {
        "Value": Union[datetime, str],
        "ParameterName": str,
        "TimeGranularity": TimeGranularityType,
    },
    total=False,
)


class TimeEqualityFilterTypeDef(
    _RequiredTimeEqualityFilterTypeDef, _OptionalTimeEqualityFilterTypeDef
):
    pass


TimeRangeDrillDownFilterTypeDef = TypedDict(
    "TimeRangeDrillDownFilterTypeDef",
    {
        "Column": ColumnIdentifierTypeDef,
        "RangeMinimum": Union[datetime, str],
        "RangeMaximum": Union[datetime, str],
        "TimeGranularity": TimeGranularityType,
    },
)

AnalysisErrorTypeDef = TypedDict(
    "AnalysisErrorTypeDef",
    {
        "Type": AnalysisErrorTypeType,
        "Message": str,
        "ViolatedEntities": List[EntityTypeDef],
    },
    total=False,
)

DashboardErrorTypeDef = TypedDict(
    "DashboardErrorTypeDef",
    {
        "Type": DashboardErrorTypeType,
        "Message": str,
        "ViolatedEntities": List[EntityTypeDef],
    },
    total=False,
)

TemplateErrorTypeDef = TypedDict(
    "TemplateErrorTypeDef",
    {
        "Type": TemplateErrorTypeType,
        "Message": str,
        "ViolatedEntities": List[EntityTypeDef],
    },
    total=False,
)

_RequiredSearchAnalysesRequestRequestTypeDef = TypedDict(
    "_RequiredSearchAnalysesRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "Filters": Sequence[AnalysisSearchFilterTypeDef],
    },
)
_OptionalSearchAnalysesRequestRequestTypeDef = TypedDict(
    "_OptionalSearchAnalysesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class SearchAnalysesRequestRequestTypeDef(
    _RequiredSearchAnalysesRequestRequestTypeDef, _OptionalSearchAnalysesRequestRequestTypeDef
):
    pass


AnalysisSourceTemplateTypeDef = TypedDict(
    "AnalysisSourceTemplateTypeDef",
    {
        "DataSetReferences": Sequence[DataSetReferenceTypeDef],
        "Arn": str,
    },
)

DashboardSourceTemplateTypeDef = TypedDict(
    "DashboardSourceTemplateTypeDef",
    {
        "DataSetReferences": Sequence[DataSetReferenceTypeDef],
        "Arn": str,
    },
)

TemplateSourceAnalysisTypeDef = TypedDict(
    "TemplateSourceAnalysisTypeDef",
    {
        "Arn": str,
        "DataSetReferences": Sequence[DataSetReferenceTypeDef],
    },
)

AnonymousUserDashboardVisualEmbeddingConfigurationTypeDef = TypedDict(
    "AnonymousUserDashboardVisualEmbeddingConfigurationTypeDef",
    {
        "InitialDashboardVisualId": DashboardVisualIdTypeDef,
    },
)

RegisteredUserDashboardVisualEmbeddingConfigurationTypeDef = TypedDict(
    "RegisteredUserDashboardVisualEmbeddingConfigurationTypeDef",
    {
        "InitialDashboardVisualId": DashboardVisualIdTypeDef,
    },
)

ArcAxisConfigurationTypeDef = TypedDict(
    "ArcAxisConfigurationTypeDef",
    {
        "Range": ArcAxisDisplayRangeTypeDef,
        "ReserveRange": int,
    },
    total=False,
)

AxisDisplayRangeTypeDef = TypedDict(
    "AxisDisplayRangeTypeDef",
    {
        "MinMax": AxisDisplayMinMaxRangeTypeDef,
        "DataDriven": Mapping[str, Any],
    },
    total=False,
)

AxisScaleTypeDef = TypedDict(
    "AxisScaleTypeDef",
    {
        "Linear": AxisLinearScaleTypeDef,
        "Logarithmic": AxisLogarithmicScaleTypeDef,
    },
    total=False,
)

HistogramBinOptionsTypeDef = TypedDict(
    "HistogramBinOptionsTypeDef",
    {
        "SelectedBinType": HistogramBinTypeType,
        "BinCount": BinCountOptionsTypeDef,
        "BinWidth": BinWidthOptionsTypeDef,
        "StartValue": float,
    },
    total=False,
)

TileStyleTypeDef = TypedDict(
    "TileStyleTypeDef",
    {
        "Border": BorderStyleTypeDef,
    },
    total=False,
)

BoxPlotOptionsTypeDef = TypedDict(
    "BoxPlotOptionsTypeDef",
    {
        "StyleOptions": BoxPlotStyleOptionsTypeDef,
        "OutlierVisibility": VisibilityType,
        "AllDataPointsVisibility": VisibilityType,
    },
    total=False,
)

CreateColumnsOperationTypeDef = TypedDict(
    "CreateColumnsOperationTypeDef",
    {
        "Columns": Sequence[CalculatedColumnTypeDef],
    },
)

CancelIngestionResponseTypeDef = TypedDict(
    "CancelIngestionResponseTypeDef",
    {
        "Arn": str,
        "IngestionId": str,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateAccountCustomizationResponseTypeDef = TypedDict(
    "CreateAccountCustomizationResponseTypeDef",
    {
        "Arn": str,
        "AwsAccountId": str,
        "Namespace": str,
        "AccountCustomization": AccountCustomizationTypeDef,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateAnalysisResponseTypeDef = TypedDict(
    "CreateAnalysisResponseTypeDef",
    {
        "Arn": str,
        "AnalysisId": str,
        "CreationStatus": ResourceStatusType,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDashboardResponseTypeDef = TypedDict(
    "CreateDashboardResponseTypeDef",
    {
        "Arn": str,
        "VersionArn": str,
        "DashboardId": str,
        "CreationStatus": ResourceStatusType,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDataSetResponseTypeDef = TypedDict(
    "CreateDataSetResponseTypeDef",
    {
        "Arn": str,
        "DataSetId": str,
        "IngestionArn": str,
        "IngestionId": str,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDataSourceResponseTypeDef = TypedDict(
    "CreateDataSourceResponseTypeDef",
    {
        "Arn": str,
        "DataSourceId": str,
        "CreationStatus": ResourceStatusType,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateFolderResponseTypeDef = TypedDict(
    "CreateFolderResponseTypeDef",
    {
        "Status": int,
        "Arn": str,
        "FolderId": str,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateIAMPolicyAssignmentResponseTypeDef = TypedDict(
    "CreateIAMPolicyAssignmentResponseTypeDef",
    {
        "AssignmentName": str,
        "AssignmentId": str,
        "AssignmentStatus": AssignmentStatusType,
        "PolicyArn": str,
        "Identities": Dict[str, List[str]],
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateIngestionResponseTypeDef = TypedDict(
    "CreateIngestionResponseTypeDef",
    {
        "Arn": str,
        "IngestionId": str,
        "IngestionStatus": IngestionStatusType,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateNamespaceResponseTypeDef = TypedDict(
    "CreateNamespaceResponseTypeDef",
    {
        "Arn": str,
        "Name": str,
        "CapacityRegion": str,
        "CreationStatus": NamespaceStatusType,
        "IdentityStore": Literal["QUICKSIGHT"],
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateRefreshScheduleResponseTypeDef = TypedDict(
    "CreateRefreshScheduleResponseTypeDef",
    {
        "Status": int,
        "RequestId": str,
        "ScheduleId": str,
        "Arn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateTemplateResponseTypeDef = TypedDict(
    "CreateTemplateResponseTypeDef",
    {
        "Arn": str,
        "VersionArn": str,
        "TemplateId": str,
        "CreationStatus": ResourceStatusType,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateThemeResponseTypeDef = TypedDict(
    "CreateThemeResponseTypeDef",
    {
        "Arn": str,
        "VersionArn": str,
        "ThemeId": str,
        "CreationStatus": ResourceStatusType,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteAccountCustomizationResponseTypeDef = TypedDict(
    "DeleteAccountCustomizationResponseTypeDef",
    {
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteAccountSubscriptionResponseTypeDef = TypedDict(
    "DeleteAccountSubscriptionResponseTypeDef",
    {
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteAnalysisResponseTypeDef = TypedDict(
    "DeleteAnalysisResponseTypeDef",
    {
        "Status": int,
        "Arn": str,
        "AnalysisId": str,
        "DeletionTime": datetime,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteDashboardResponseTypeDef = TypedDict(
    "DeleteDashboardResponseTypeDef",
    {
        "Status": int,
        "Arn": str,
        "DashboardId": str,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteDataSetRefreshPropertiesResponseTypeDef = TypedDict(
    "DeleteDataSetRefreshPropertiesResponseTypeDef",
    {
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteDataSetResponseTypeDef = TypedDict(
    "DeleteDataSetResponseTypeDef",
    {
        "Arn": str,
        "DataSetId": str,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteDataSourceResponseTypeDef = TypedDict(
    "DeleteDataSourceResponseTypeDef",
    {
        "Arn": str,
        "DataSourceId": str,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteFolderMembershipResponseTypeDef = TypedDict(
    "DeleteFolderMembershipResponseTypeDef",
    {
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteFolderResponseTypeDef = TypedDict(
    "DeleteFolderResponseTypeDef",
    {
        "Status": int,
        "Arn": str,
        "FolderId": str,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteGroupMembershipResponseTypeDef = TypedDict(
    "DeleteGroupMembershipResponseTypeDef",
    {
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteGroupResponseTypeDef = TypedDict(
    "DeleteGroupResponseTypeDef",
    {
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteIAMPolicyAssignmentResponseTypeDef = TypedDict(
    "DeleteIAMPolicyAssignmentResponseTypeDef",
    {
        "AssignmentName": str,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteNamespaceResponseTypeDef = TypedDict(
    "DeleteNamespaceResponseTypeDef",
    {
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteRefreshScheduleResponseTypeDef = TypedDict(
    "DeleteRefreshScheduleResponseTypeDef",
    {
        "Status": int,
        "RequestId": str,
        "ScheduleId": str,
        "Arn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteTemplateAliasResponseTypeDef = TypedDict(
    "DeleteTemplateAliasResponseTypeDef",
    {
        "Status": int,
        "TemplateId": str,
        "AliasName": str,
        "Arn": str,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteTemplateResponseTypeDef = TypedDict(
    "DeleteTemplateResponseTypeDef",
    {
        "RequestId": str,
        "Arn": str,
        "TemplateId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteThemeAliasResponseTypeDef = TypedDict(
    "DeleteThemeAliasResponseTypeDef",
    {
        "AliasName": str,
        "Arn": str,
        "RequestId": str,
        "Status": int,
        "ThemeId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteThemeResponseTypeDef = TypedDict(
    "DeleteThemeResponseTypeDef",
    {
        "Arn": str,
        "RequestId": str,
        "Status": int,
        "ThemeId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteUserByPrincipalIdResponseTypeDef = TypedDict(
    "DeleteUserByPrincipalIdResponseTypeDef",
    {
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteUserResponseTypeDef = TypedDict(
    "DeleteUserResponseTypeDef",
    {
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeAccountCustomizationResponseTypeDef = TypedDict(
    "DescribeAccountCustomizationResponseTypeDef",
    {
        "Arn": str,
        "AwsAccountId": str,
        "Namespace": str,
        "AccountCustomization": AccountCustomizationTypeDef,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeAccountSettingsResponseTypeDef = TypedDict(
    "DescribeAccountSettingsResponseTypeDef",
    {
        "AccountSettings": AccountSettingsTypeDef,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeAccountSubscriptionResponseTypeDef = TypedDict(
    "DescribeAccountSubscriptionResponseTypeDef",
    {
        "AccountInfo": AccountInfoTypeDef,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeIpRestrictionResponseTypeDef = TypedDict(
    "DescribeIpRestrictionResponseTypeDef",
    {
        "AwsAccountId": str,
        "IpRestrictionRuleMap": Dict[str, str],
        "Enabled": bool,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GenerateEmbedUrlForAnonymousUserResponseTypeDef = TypedDict(
    "GenerateEmbedUrlForAnonymousUserResponseTypeDef",
    {
        "EmbedUrl": str,
        "Status": int,
        "RequestId": str,
        "AnonymousUserArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GenerateEmbedUrlForRegisteredUserResponseTypeDef = TypedDict(
    "GenerateEmbedUrlForRegisteredUserResponseTypeDef",
    {
        "EmbedUrl": str,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetDashboardEmbedUrlResponseTypeDef = TypedDict(
    "GetDashboardEmbedUrlResponseTypeDef",
    {
        "EmbedUrl": str,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSessionEmbedUrlResponseTypeDef = TypedDict(
    "GetSessionEmbedUrlResponseTypeDef",
    {
        "EmbedUrl": str,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAnalysesResponseTypeDef = TypedDict(
    "ListAnalysesResponseTypeDef",
    {
        "AnalysisSummaryList": List[AnalysisSummaryTypeDef],
        "NextToken": str,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListIAMPolicyAssignmentsForUserResponseTypeDef = TypedDict(
    "ListIAMPolicyAssignmentsForUserResponseTypeDef",
    {
        "ActiveAssignments": List[ActiveIAMPolicyAssignmentTypeDef],
        "RequestId": str,
        "NextToken": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutDataSetRefreshPropertiesResponseTypeDef = TypedDict(
    "PutDataSetRefreshPropertiesResponseTypeDef",
    {
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RestoreAnalysisResponseTypeDef = TypedDict(
    "RestoreAnalysisResponseTypeDef",
    {
        "Status": int,
        "Arn": str,
        "AnalysisId": str,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SearchAnalysesResponseTypeDef = TypedDict(
    "SearchAnalysesResponseTypeDef",
    {
        "AnalysisSummaryList": List[AnalysisSummaryTypeDef],
        "NextToken": str,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TagResourceResponseTypeDef = TypedDict(
    "TagResourceResponseTypeDef",
    {
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UntagResourceResponseTypeDef = TypedDict(
    "UntagResourceResponseTypeDef",
    {
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateAccountCustomizationResponseTypeDef = TypedDict(
    "UpdateAccountCustomizationResponseTypeDef",
    {
        "Arn": str,
        "AwsAccountId": str,
        "Namespace": str,
        "AccountCustomization": AccountCustomizationTypeDef,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateAccountSettingsResponseTypeDef = TypedDict(
    "UpdateAccountSettingsResponseTypeDef",
    {
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateAnalysisResponseTypeDef = TypedDict(
    "UpdateAnalysisResponseTypeDef",
    {
        "Arn": str,
        "AnalysisId": str,
        "UpdateStatus": ResourceStatusType,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateDashboardPublishedVersionResponseTypeDef = TypedDict(
    "UpdateDashboardPublishedVersionResponseTypeDef",
    {
        "DashboardId": str,
        "DashboardArn": str,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateDashboardResponseTypeDef = TypedDict(
    "UpdateDashboardResponseTypeDef",
    {
        "Arn": str,
        "VersionArn": str,
        "DashboardId": str,
        "CreationStatus": ResourceStatusType,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateDataSetPermissionsResponseTypeDef = TypedDict(
    "UpdateDataSetPermissionsResponseTypeDef",
    {
        "DataSetArn": str,
        "DataSetId": str,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateDataSetResponseTypeDef = TypedDict(
    "UpdateDataSetResponseTypeDef",
    {
        "Arn": str,
        "DataSetId": str,
        "IngestionArn": str,
        "IngestionId": str,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateDataSourcePermissionsResponseTypeDef = TypedDict(
    "UpdateDataSourcePermissionsResponseTypeDef",
    {
        "DataSourceArn": str,
        "DataSourceId": str,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateDataSourceResponseTypeDef = TypedDict(
    "UpdateDataSourceResponseTypeDef",
    {
        "Arn": str,
        "DataSourceId": str,
        "UpdateStatus": ResourceStatusType,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateFolderResponseTypeDef = TypedDict(
    "UpdateFolderResponseTypeDef",
    {
        "Status": int,
        "Arn": str,
        "FolderId": str,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateIAMPolicyAssignmentResponseTypeDef = TypedDict(
    "UpdateIAMPolicyAssignmentResponseTypeDef",
    {
        "AssignmentName": str,
        "AssignmentId": str,
        "PolicyArn": str,
        "Identities": Dict[str, List[str]],
        "AssignmentStatus": AssignmentStatusType,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateIpRestrictionResponseTypeDef = TypedDict(
    "UpdateIpRestrictionResponseTypeDef",
    {
        "AwsAccountId": str,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdatePublicSharingSettingsResponseTypeDef = TypedDict(
    "UpdatePublicSharingSettingsResponseTypeDef",
    {
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateRefreshScheduleResponseTypeDef = TypedDict(
    "UpdateRefreshScheduleResponseTypeDef",
    {
        "Status": int,
        "RequestId": str,
        "ScheduleId": str,
        "Arn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateTemplateResponseTypeDef = TypedDict(
    "UpdateTemplateResponseTypeDef",
    {
        "TemplateId": str,
        "Arn": str,
        "VersionArn": str,
        "CreationStatus": ResourceStatusType,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateThemeResponseTypeDef = TypedDict(
    "UpdateThemeResponseTypeDef",
    {
        "ThemeId": str,
        "Arn": str,
        "VersionArn": str,
        "CreationStatus": ResourceStatusType,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CategoryFilterConfigurationTypeDef = TypedDict(
    "CategoryFilterConfigurationTypeDef",
    {
        "FilterListConfiguration": FilterListConfigurationTypeDef,
        "CustomFilterListConfiguration": CustomFilterListConfigurationTypeDef,
        "CustomFilterConfiguration": CustomFilterConfigurationTypeDef,
    },
    total=False,
)

ClusterMarkerTypeDef = TypedDict(
    "ClusterMarkerTypeDef",
    {
        "SimpleClusterMarker": SimpleClusterMarkerTypeDef,
    },
    total=False,
)

_RequiredColorScaleTypeDef = TypedDict(
    "_RequiredColorScaleTypeDef",
    {
        "Colors": Sequence[DataColorTypeDef],
        "ColorFillType": ColorFillTypeType,
    },
)
_OptionalColorScaleTypeDef = TypedDict(
    "_OptionalColorScaleTypeDef",
    {
        "NullValueColor": DataColorTypeDef,
    },
    total=False,
)


class ColorScaleTypeDef(_RequiredColorScaleTypeDef, _OptionalColorScaleTypeDef):
    pass


ColumnTagTypeDef = TypedDict(
    "ColumnTagTypeDef",
    {
        "ColumnGeographicRole": GeoSpatialDataRoleType,
        "ColumnDescription": ColumnDescriptionTypeDef,
    },
    total=False,
)

ColumnGroupSchemaTypeDef = TypedDict(
    "ColumnGroupSchemaTypeDef",
    {
        "Name": str,
        "ColumnGroupColumnSchemaList": Sequence[ColumnGroupColumnSchemaTypeDef],
    },
    total=False,
)

ColumnGroupTypeDef = TypedDict(
    "ColumnGroupTypeDef",
    {
        "GeoSpatialColumnGroup": GeoSpatialColumnGroupTypeDef,
    },
    total=False,
)

DataSetSchemaTypeDef = TypedDict(
    "DataSetSchemaTypeDef",
    {
        "ColumnSchemaList": Sequence[ColumnSchemaTypeDef],
    },
    total=False,
)

_RequiredConditionalFormattingCustomIconConditionTypeDef = TypedDict(
    "_RequiredConditionalFormattingCustomIconConditionTypeDef",
    {
        "Expression": str,
        "IconOptions": ConditionalFormattingCustomIconOptionsTypeDef,
    },
)
_OptionalConditionalFormattingCustomIconConditionTypeDef = TypedDict(
    "_OptionalConditionalFormattingCustomIconConditionTypeDef",
    {
        "Color": str,
        "DisplayConfiguration": ConditionalFormattingIconDisplayConfigurationTypeDef,
    },
    total=False,
)


class ConditionalFormattingCustomIconConditionTypeDef(
    _RequiredConditionalFormattingCustomIconConditionTypeDef,
    _OptionalConditionalFormattingCustomIconConditionTypeDef,
):
    pass


_RequiredCreateAccountCustomizationRequestRequestTypeDef = TypedDict(
    "_RequiredCreateAccountCustomizationRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "AccountCustomization": AccountCustomizationTypeDef,
    },
)
_OptionalCreateAccountCustomizationRequestRequestTypeDef = TypedDict(
    "_OptionalCreateAccountCustomizationRequestRequestTypeDef",
    {
        "Namespace": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateAccountCustomizationRequestRequestTypeDef(
    _RequiredCreateAccountCustomizationRequestRequestTypeDef,
    _OptionalCreateAccountCustomizationRequestRequestTypeDef,
):
    pass


_RequiredCreateNamespaceRequestRequestTypeDef = TypedDict(
    "_RequiredCreateNamespaceRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "Namespace": str,
        "IdentityStore": Literal["QUICKSIGHT"],
    },
)
_OptionalCreateNamespaceRequestRequestTypeDef = TypedDict(
    "_OptionalCreateNamespaceRequestRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateNamespaceRequestRequestTypeDef(
    _RequiredCreateNamespaceRequestRequestTypeDef, _OptionalCreateNamespaceRequestRequestTypeDef
):
    pass


ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "Tags": List[TagTypeDef],
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "Tags": Sequence[TagTypeDef],
    },
)

CreateAccountSubscriptionResponseTypeDef = TypedDict(
    "CreateAccountSubscriptionResponseTypeDef",
    {
        "SignupResponse": SignupResponseTypeDef,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateFolderRequestRequestTypeDef = TypedDict(
    "_RequiredCreateFolderRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "FolderId": str,
    },
)
_OptionalCreateFolderRequestRequestTypeDef = TypedDict(
    "_OptionalCreateFolderRequestRequestTypeDef",
    {
        "Name": str,
        "FolderType": Literal["SHARED"],
        "ParentFolderArn": str,
        "Permissions": Sequence[ResourcePermissionTypeDef],
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateFolderRequestRequestTypeDef(
    _RequiredCreateFolderRequestRequestTypeDef, _OptionalCreateFolderRequestRequestTypeDef
):
    pass


DescribeAnalysisPermissionsResponseTypeDef = TypedDict(
    "DescribeAnalysisPermissionsResponseTypeDef",
    {
        "AnalysisId": str,
        "AnalysisArn": str,
        "Permissions": List[ResourcePermissionTypeDef],
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeDataSetPermissionsResponseTypeDef = TypedDict(
    "DescribeDataSetPermissionsResponseTypeDef",
    {
        "DataSetArn": str,
        "DataSetId": str,
        "Permissions": List[ResourcePermissionTypeDef],
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeDataSourcePermissionsResponseTypeDef = TypedDict(
    "DescribeDataSourcePermissionsResponseTypeDef",
    {
        "DataSourceArn": str,
        "DataSourceId": str,
        "Permissions": List[ResourcePermissionTypeDef],
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeFolderPermissionsResponseTypeDef = TypedDict(
    "DescribeFolderPermissionsResponseTypeDef",
    {
        "Status": int,
        "FolderId": str,
        "Arn": str,
        "Permissions": List[ResourcePermissionTypeDef],
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeFolderResolvedPermissionsResponseTypeDef = TypedDict(
    "DescribeFolderResolvedPermissionsResponseTypeDef",
    {
        "Status": int,
        "FolderId": str,
        "Arn": str,
        "Permissions": List[ResourcePermissionTypeDef],
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeTemplatePermissionsResponseTypeDef = TypedDict(
    "DescribeTemplatePermissionsResponseTypeDef",
    {
        "TemplateId": str,
        "TemplateArn": str,
        "Permissions": List[ResourcePermissionTypeDef],
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeThemePermissionsResponseTypeDef = TypedDict(
    "DescribeThemePermissionsResponseTypeDef",
    {
        "ThemeId": str,
        "ThemeArn": str,
        "Permissions": List[ResourcePermissionTypeDef],
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

LinkSharingConfigurationTypeDef = TypedDict(
    "LinkSharingConfigurationTypeDef",
    {
        "Permissions": List[ResourcePermissionTypeDef],
    },
    total=False,
)

_RequiredUpdateAnalysisPermissionsRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateAnalysisPermissionsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "AnalysisId": str,
    },
)
_OptionalUpdateAnalysisPermissionsRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateAnalysisPermissionsRequestRequestTypeDef",
    {
        "GrantPermissions": Sequence[ResourcePermissionTypeDef],
        "RevokePermissions": Sequence[ResourcePermissionTypeDef],
    },
    total=False,
)


class UpdateAnalysisPermissionsRequestRequestTypeDef(
    _RequiredUpdateAnalysisPermissionsRequestRequestTypeDef,
    _OptionalUpdateAnalysisPermissionsRequestRequestTypeDef,
):
    pass


UpdateAnalysisPermissionsResponseTypeDef = TypedDict(
    "UpdateAnalysisPermissionsResponseTypeDef",
    {
        "AnalysisArn": str,
        "AnalysisId": str,
        "Permissions": List[ResourcePermissionTypeDef],
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdateDashboardPermissionsRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateDashboardPermissionsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DashboardId": str,
    },
)
_OptionalUpdateDashboardPermissionsRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateDashboardPermissionsRequestRequestTypeDef",
    {
        "GrantPermissions": Sequence[ResourcePermissionTypeDef],
        "RevokePermissions": Sequence[ResourcePermissionTypeDef],
        "GrantLinkPermissions": Sequence[ResourcePermissionTypeDef],
        "RevokeLinkPermissions": Sequence[ResourcePermissionTypeDef],
    },
    total=False,
)


class UpdateDashboardPermissionsRequestRequestTypeDef(
    _RequiredUpdateDashboardPermissionsRequestRequestTypeDef,
    _OptionalUpdateDashboardPermissionsRequestRequestTypeDef,
):
    pass


_RequiredUpdateDataSetPermissionsRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateDataSetPermissionsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DataSetId": str,
    },
)
_OptionalUpdateDataSetPermissionsRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateDataSetPermissionsRequestRequestTypeDef",
    {
        "GrantPermissions": Sequence[ResourcePermissionTypeDef],
        "RevokePermissions": Sequence[ResourcePermissionTypeDef],
    },
    total=False,
)


class UpdateDataSetPermissionsRequestRequestTypeDef(
    _RequiredUpdateDataSetPermissionsRequestRequestTypeDef,
    _OptionalUpdateDataSetPermissionsRequestRequestTypeDef,
):
    pass


_RequiredUpdateDataSourcePermissionsRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateDataSourcePermissionsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DataSourceId": str,
    },
)
_OptionalUpdateDataSourcePermissionsRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateDataSourcePermissionsRequestRequestTypeDef",
    {
        "GrantPermissions": Sequence[ResourcePermissionTypeDef],
        "RevokePermissions": Sequence[ResourcePermissionTypeDef],
    },
    total=False,
)


class UpdateDataSourcePermissionsRequestRequestTypeDef(
    _RequiredUpdateDataSourcePermissionsRequestRequestTypeDef,
    _OptionalUpdateDataSourcePermissionsRequestRequestTypeDef,
):
    pass


_RequiredUpdateFolderPermissionsRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateFolderPermissionsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "FolderId": str,
    },
)
_OptionalUpdateFolderPermissionsRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateFolderPermissionsRequestRequestTypeDef",
    {
        "GrantPermissions": Sequence[ResourcePermissionTypeDef],
        "RevokePermissions": Sequence[ResourcePermissionTypeDef],
    },
    total=False,
)


class UpdateFolderPermissionsRequestRequestTypeDef(
    _RequiredUpdateFolderPermissionsRequestRequestTypeDef,
    _OptionalUpdateFolderPermissionsRequestRequestTypeDef,
):
    pass


UpdateFolderPermissionsResponseTypeDef = TypedDict(
    "UpdateFolderPermissionsResponseTypeDef",
    {
        "Status": int,
        "Arn": str,
        "FolderId": str,
        "Permissions": List[ResourcePermissionTypeDef],
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdateTemplatePermissionsRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateTemplatePermissionsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "TemplateId": str,
    },
)
_OptionalUpdateTemplatePermissionsRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateTemplatePermissionsRequestRequestTypeDef",
    {
        "GrantPermissions": Sequence[ResourcePermissionTypeDef],
        "RevokePermissions": Sequence[ResourcePermissionTypeDef],
    },
    total=False,
)


class UpdateTemplatePermissionsRequestRequestTypeDef(
    _RequiredUpdateTemplatePermissionsRequestRequestTypeDef,
    _OptionalUpdateTemplatePermissionsRequestRequestTypeDef,
):
    pass


UpdateTemplatePermissionsResponseTypeDef = TypedDict(
    "UpdateTemplatePermissionsResponseTypeDef",
    {
        "TemplateId": str,
        "TemplateArn": str,
        "Permissions": List[ResourcePermissionTypeDef],
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdateThemePermissionsRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateThemePermissionsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "ThemeId": str,
    },
)
_OptionalUpdateThemePermissionsRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateThemePermissionsRequestRequestTypeDef",
    {
        "GrantPermissions": Sequence[ResourcePermissionTypeDef],
        "RevokePermissions": Sequence[ResourcePermissionTypeDef],
    },
    total=False,
)


class UpdateThemePermissionsRequestRequestTypeDef(
    _RequiredUpdateThemePermissionsRequestRequestTypeDef,
    _OptionalUpdateThemePermissionsRequestRequestTypeDef,
):
    pass


UpdateThemePermissionsResponseTypeDef = TypedDict(
    "UpdateThemePermissionsResponseTypeDef",
    {
        "ThemeId": str,
        "ThemeArn": str,
        "Permissions": List[ResourcePermissionTypeDef],
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DataSetSummaryTypeDef = TypedDict(
    "DataSetSummaryTypeDef",
    {
        "Arn": str,
        "DataSetId": str,
        "Name": str,
        "CreatedTime": datetime,
        "LastUpdatedTime": datetime,
        "ImportMode": DataSetImportModeType,
        "RowLevelPermissionDataSet": RowLevelPermissionDataSetTypeDef,
        "RowLevelPermissionTagConfigurationApplied": bool,
        "ColumnLevelPermissionRulesApplied": bool,
    },
    total=False,
)

CreateFolderMembershipResponseTypeDef = TypedDict(
    "CreateFolderMembershipResponseTypeDef",
    {
        "Status": int,
        "FolderMember": FolderMemberTypeDef,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateGroupMembershipResponseTypeDef = TypedDict(
    "CreateGroupMembershipResponseTypeDef",
    {
        "GroupMember": GroupMemberTypeDef,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeGroupMembershipResponseTypeDef = TypedDict(
    "DescribeGroupMembershipResponseTypeDef",
    {
        "GroupMember": GroupMemberTypeDef,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListGroupMembershipsResponseTypeDef = TypedDict(
    "ListGroupMembershipsResponseTypeDef",
    {
        "GroupMemberList": List[GroupMemberTypeDef],
        "NextToken": str,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateGroupResponseTypeDef = TypedDict(
    "CreateGroupResponseTypeDef",
    {
        "Group": GroupTypeDef,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeGroupResponseTypeDef = TypedDict(
    "DescribeGroupResponseTypeDef",
    {
        "Group": GroupTypeDef,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListGroupsResponseTypeDef = TypedDict(
    "ListGroupsResponseTypeDef",
    {
        "GroupList": List[GroupTypeDef],
        "NextToken": str,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListUserGroupsResponseTypeDef = TypedDict(
    "ListUserGroupsResponseTypeDef",
    {
        "GroupList": List[GroupTypeDef],
        "NextToken": str,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SearchGroupsResponseTypeDef = TypedDict(
    "SearchGroupsResponseTypeDef",
    {
        "GroupList": List[GroupTypeDef],
        "NextToken": str,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateGroupResponseTypeDef = TypedDict(
    "UpdateGroupResponseTypeDef",
    {
        "Group": GroupTypeDef,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateTemplateAliasResponseTypeDef = TypedDict(
    "CreateTemplateAliasResponseTypeDef",
    {
        "TemplateAlias": TemplateAliasTypeDef,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeTemplateAliasResponseTypeDef = TypedDict(
    "DescribeTemplateAliasResponseTypeDef",
    {
        "TemplateAlias": TemplateAliasTypeDef,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTemplateAliasesResponseTypeDef = TypedDict(
    "ListTemplateAliasesResponseTypeDef",
    {
        "TemplateAliasList": List[TemplateAliasTypeDef],
        "Status": int,
        "RequestId": str,
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateTemplateAliasResponseTypeDef = TypedDict(
    "UpdateTemplateAliasResponseTypeDef",
    {
        "TemplateAlias": TemplateAliasTypeDef,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateThemeAliasResponseTypeDef = TypedDict(
    "CreateThemeAliasResponseTypeDef",
    {
        "ThemeAlias": ThemeAliasTypeDef,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeThemeAliasResponseTypeDef = TypedDict(
    "DescribeThemeAliasResponseTypeDef",
    {
        "ThemeAlias": ThemeAliasTypeDef,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListThemeAliasesResponseTypeDef = TypedDict(
    "ListThemeAliasesResponseTypeDef",
    {
        "ThemeAliasList": List[ThemeAliasTypeDef],
        "Status": int,
        "RequestId": str,
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateThemeAliasResponseTypeDef = TypedDict(
    "UpdateThemeAliasResponseTypeDef",
    {
        "ThemeAlias": ThemeAliasTypeDef,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CustomActionNavigationOperationTypeDef = TypedDict(
    "CustomActionNavigationOperationTypeDef",
    {
        "LocalNavigationConfiguration": LocalNavigationConfigurationTypeDef,
    },
    total=False,
)

_RequiredCustomValuesConfigurationTypeDef = TypedDict(
    "_RequiredCustomValuesConfigurationTypeDef",
    {
        "CustomValues": CustomParameterValuesTypeDef,
    },
)
_OptionalCustomValuesConfigurationTypeDef = TypedDict(
    "_OptionalCustomValuesConfigurationTypeDef",
    {
        "IncludeNullValue": bool,
    },
    total=False,
)


class CustomValuesConfigurationTypeDef(
    _RequiredCustomValuesConfigurationTypeDef, _OptionalCustomValuesConfigurationTypeDef
):
    pass


_RequiredCustomSqlTypeDef = TypedDict(
    "_RequiredCustomSqlTypeDef",
    {
        "DataSourceArn": str,
        "Name": str,
        "SqlQuery": str,
    },
)
_OptionalCustomSqlTypeDef = TypedDict(
    "_OptionalCustomSqlTypeDef",
    {
        "Columns": Sequence[InputColumnTypeDef],
    },
    total=False,
)


class CustomSqlTypeDef(_RequiredCustomSqlTypeDef, _OptionalCustomSqlTypeDef):
    pass


_RequiredRelationalTableTypeDef = TypedDict(
    "_RequiredRelationalTableTypeDef",
    {
        "DataSourceArn": str,
        "Name": str,
        "InputColumns": Sequence[InputColumnTypeDef],
    },
)
_OptionalRelationalTableTypeDef = TypedDict(
    "_OptionalRelationalTableTypeDef",
    {
        "Catalog": str,
        "Schema": str,
    },
    total=False,
)


class RelationalTableTypeDef(_RequiredRelationalTableTypeDef, _OptionalRelationalTableTypeDef):
    pass


_RequiredSearchDashboardsRequestRequestTypeDef = TypedDict(
    "_RequiredSearchDashboardsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "Filters": Sequence[DashboardSearchFilterTypeDef],
    },
)
_OptionalSearchDashboardsRequestRequestTypeDef = TypedDict(
    "_OptionalSearchDashboardsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class SearchDashboardsRequestRequestTypeDef(
    _RequiredSearchDashboardsRequestRequestTypeDef, _OptionalSearchDashboardsRequestRequestTypeDef
):
    pass


ListDashboardsResponseTypeDef = TypedDict(
    "ListDashboardsResponseTypeDef",
    {
        "DashboardSummaryList": List[DashboardSummaryTypeDef],
        "NextToken": str,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SearchDashboardsResponseTypeDef = TypedDict(
    "SearchDashboardsResponseTypeDef",
    {
        "DashboardSummaryList": List[DashboardSummaryTypeDef],
        "NextToken": str,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListDashboardVersionsResponseTypeDef = TypedDict(
    "ListDashboardVersionsResponseTypeDef",
    {
        "DashboardVersionSummaryList": List[DashboardVersionSummaryTypeDef],
        "NextToken": str,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DashboardVisualPublishOptionsTypeDef = TypedDict(
    "DashboardVisualPublishOptionsTypeDef",
    {
        "ExportHiddenFieldsOption": ExportHiddenFieldsOptionTypeDef,
    },
    total=False,
)

TableInlineVisualizationTypeDef = TypedDict(
    "TableInlineVisualizationTypeDef",
    {
        "DataBars": DataBarsOptionsTypeDef,
    },
    total=False,
)

DataLabelTypeTypeDef = TypedDict(
    "DataLabelTypeTypeDef",
    {
        "FieldLabelType": FieldLabelTypeTypeDef,
        "DataPathLabelType": DataPathLabelTypeTypeDef,
        "RangeEndsLabelType": RangeEndsLabelTypeTypeDef,
        "MinimumLabelType": MinimumLabelTypeTypeDef,
        "MaximumLabelType": MaximumLabelTypeTypeDef,
    },
    total=False,
)

_RequiredDataPathColorTypeDef = TypedDict(
    "_RequiredDataPathColorTypeDef",
    {
        "Element": DataPathValueTypeDef,
        "Color": str,
    },
)
_OptionalDataPathColorTypeDef = TypedDict(
    "_OptionalDataPathColorTypeDef",
    {
        "TimeGranularity": TimeGranularityType,
    },
    total=False,
)


class DataPathColorTypeDef(_RequiredDataPathColorTypeDef, _OptionalDataPathColorTypeDef):
    pass


DataPathSortTypeDef = TypedDict(
    "DataPathSortTypeDef",
    {
        "Direction": SortDirectionType,
        "SortPaths": Sequence[DataPathValueTypeDef],
    },
)

_RequiredPivotTableDataPathOptionTypeDef = TypedDict(
    "_RequiredPivotTableDataPathOptionTypeDef",
    {
        "DataPathList": Sequence[DataPathValueTypeDef],
    },
)
_OptionalPivotTableDataPathOptionTypeDef = TypedDict(
    "_OptionalPivotTableDataPathOptionTypeDef",
    {
        "Width": str,
    },
    total=False,
)


class PivotTableDataPathOptionTypeDef(
    _RequiredPivotTableDataPathOptionTypeDef, _OptionalPivotTableDataPathOptionTypeDef
):
    pass


_RequiredSearchDataSetsRequestRequestTypeDef = TypedDict(
    "_RequiredSearchDataSetsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "Filters": Sequence[DataSetSearchFilterTypeDef],
    },
)
_OptionalSearchDataSetsRequestRequestTypeDef = TypedDict(
    "_OptionalSearchDataSetsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class SearchDataSetsRequestRequestTypeDef(
    _RequiredSearchDataSetsRequestRequestTypeDef, _OptionalSearchDataSetsRequestRequestTypeDef
):
    pass


_RequiredSearchDataSourcesRequestRequestTypeDef = TypedDict(
    "_RequiredSearchDataSourcesRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "Filters": Sequence[DataSourceSearchFilterTypeDef],
    },
)
_OptionalSearchDataSourcesRequestRequestTypeDef = TypedDict(
    "_OptionalSearchDataSourcesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class SearchDataSourcesRequestRequestTypeDef(
    _RequiredSearchDataSourcesRequestRequestTypeDef, _OptionalSearchDataSourcesRequestRequestTypeDef
):
    pass


SearchDataSourcesResponseTypeDef = TypedDict(
    "SearchDataSourcesResponseTypeDef",
    {
        "DataSourceSummaries": List[DataSourceSummaryTypeDef],
        "NextToken": str,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TimeRangeFilterValueTypeDef = TypedDict(
    "TimeRangeFilterValueTypeDef",
    {
        "StaticValue": Union[datetime, str],
        "RollingDate": RollingDateConfigurationTypeDef,
        "Parameter": str,
    },
    total=False,
)

DescribeFolderResponseTypeDef = TypedDict(
    "DescribeFolderResponseTypeDef",
    {
        "Status": int,
        "Folder": FolderTypeDef,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeIAMPolicyAssignmentResponseTypeDef = TypedDict(
    "DescribeIAMPolicyAssignmentResponseTypeDef",
    {
        "IAMPolicyAssignment": IAMPolicyAssignmentTypeDef,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeUserResponseTypeDef = TypedDict(
    "DescribeUserResponseTypeDef",
    {
        "User": UserTypeDef,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListUsersResponseTypeDef = TypedDict(
    "ListUsersResponseTypeDef",
    {
        "UserList": List[UserTypeDef],
        "NextToken": str,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RegisterUserResponseTypeDef = TypedDict(
    "RegisterUserResponseTypeDef",
    {
        "User": UserTypeDef,
        "UserInvitationUrl": str,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateUserResponseTypeDef = TypedDict(
    "UpdateUserResponseTypeDef",
    {
        "User": UserTypeDef,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DonutOptionsTypeDef = TypedDict(
    "DonutOptionsTypeDef",
    {
        "ArcOptions": ArcOptionsTypeDef,
        "DonutCenterOptions": DonutCenterOptionsTypeDef,
    },
    total=False,
)

_RequiredRelativeDatesFilterTypeDef = TypedDict(
    "_RequiredRelativeDatesFilterTypeDef",
    {
        "FilterId": str,
        "Column": ColumnIdentifierTypeDef,
        "AnchorDateConfiguration": AnchorDateConfigurationTypeDef,
        "TimeGranularity": TimeGranularityType,
        "RelativeDateType": RelativeDateTypeType,
        "NullOption": FilterNullOptionType,
    },
)
_OptionalRelativeDatesFilterTypeDef = TypedDict(
    "_OptionalRelativeDatesFilterTypeDef",
    {
        "MinimumGranularity": TimeGranularityType,
        "RelativeDateValue": int,
        "ParameterName": str,
        "ExcludePeriodConfiguration": ExcludePeriodConfigurationTypeDef,
    },
    total=False,
)


class RelativeDatesFilterTypeDef(
    _RequiredRelativeDatesFilterTypeDef, _OptionalRelativeDatesFilterTypeDef
):
    pass


FilterOperationTargetVisualsConfigurationTypeDef = TypedDict(
    "FilterOperationTargetVisualsConfigurationTypeDef",
    {
        "SameSheetTargetVisualConfiguration": SameSheetTargetVisualConfigurationTypeDef,
    },
    total=False,
)

_RequiredSearchFoldersRequestRequestTypeDef = TypedDict(
    "_RequiredSearchFoldersRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "Filters": Sequence[FolderSearchFilterTypeDef],
    },
)
_OptionalSearchFoldersRequestRequestTypeDef = TypedDict(
    "_OptionalSearchFoldersRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class SearchFoldersRequestRequestTypeDef(
    _RequiredSearchFoldersRequestRequestTypeDef, _OptionalSearchFoldersRequestRequestTypeDef
):
    pass


ListFoldersResponseTypeDef = TypedDict(
    "ListFoldersResponseTypeDef",
    {
        "Status": int,
        "FolderSummaryList": List[FolderSummaryTypeDef],
        "NextToken": str,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SearchFoldersResponseTypeDef = TypedDict(
    "SearchFoldersResponseTypeDef",
    {
        "Status": int,
        "FolderSummaryList": List[FolderSummaryTypeDef],
        "NextToken": str,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

FontConfigurationTypeDef = TypedDict(
    "FontConfigurationTypeDef",
    {
        "FontSize": FontSizeTypeDef,
        "FontDecoration": FontDecorationType,
        "FontColor": str,
        "FontWeight": FontWeightTypeDef,
        "FontStyle": FontStyleType,
    },
    total=False,
)

TypographyTypeDef = TypedDict(
    "TypographyTypeDef",
    {
        "FontFamilies": Sequence[FontTypeDef],
    },
    total=False,
)

ForecastScenarioTypeDef = TypedDict(
    "ForecastScenarioTypeDef",
    {
        "WhatIfPointScenario": WhatIfPointScenarioTypeDef,
        "WhatIfRangeScenario": WhatIfRangeScenarioTypeDef,
    },
    total=False,
)

FreeFormLayoutCanvasSizeOptionsTypeDef = TypedDict(
    "FreeFormLayoutCanvasSizeOptionsTypeDef",
    {
        "ScreenCanvasSizeOptions": FreeFormLayoutScreenCanvasSizeOptionsTypeDef,
    },
    total=False,
)

GeospatialWindowOptionsTypeDef = TypedDict(
    "GeospatialWindowOptionsTypeDef",
    {
        "Bounds": GeospatialCoordinateBoundsTypeDef,
        "MapZoomMode": MapZoomModeType,
    },
    total=False,
)

TableSideBorderOptionsTypeDef = TypedDict(
    "TableSideBorderOptionsTypeDef",
    {
        "InnerVertical": TableBorderOptionsTypeDef,
        "InnerHorizontal": TableBorderOptionsTypeDef,
        "Left": TableBorderOptionsTypeDef,
        "Right": TableBorderOptionsTypeDef,
        "Top": TableBorderOptionsTypeDef,
        "Bottom": TableBorderOptionsTypeDef,
    },
    total=False,
)

GradientColorTypeDef = TypedDict(
    "GradientColorTypeDef",
    {
        "Stops": Sequence[GradientStopTypeDef],
    },
    total=False,
)

GridLayoutCanvasSizeOptionsTypeDef = TypedDict(
    "GridLayoutCanvasSizeOptionsTypeDef",
    {
        "ScreenCanvasSizeOptions": GridLayoutScreenCanvasSizeOptionsTypeDef,
    },
    total=False,
)

_RequiredSearchGroupsRequestRequestTypeDef = TypedDict(
    "_RequiredSearchGroupsRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "Namespace": str,
        "Filters": Sequence[GroupSearchFilterTypeDef],
    },
)
_OptionalSearchGroupsRequestRequestTypeDef = TypedDict(
    "_OptionalSearchGroupsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class SearchGroupsRequestRequestTypeDef(
    _RequiredSearchGroupsRequestRequestTypeDef, _OptionalSearchGroupsRequestRequestTypeDef
):
    pass


ListIAMPolicyAssignmentsResponseTypeDef = TypedDict(
    "ListIAMPolicyAssignmentsResponseTypeDef",
    {
        "IAMPolicyAssignments": List[IAMPolicyAssignmentSummaryTypeDef],
        "NextToken": str,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

IncrementalRefreshTypeDef = TypedDict(
    "IncrementalRefreshTypeDef",
    {
        "LookbackWindow": LookbackWindowTypeDef,
    },
)

_RequiredIngestionTypeDef = TypedDict(
    "_RequiredIngestionTypeDef",
    {
        "Arn": str,
        "IngestionStatus": IngestionStatusType,
        "CreatedTime": datetime,
    },
)
_OptionalIngestionTypeDef = TypedDict(
    "_OptionalIngestionTypeDef",
    {
        "IngestionId": str,
        "ErrorInfo": ErrorInfoTypeDef,
        "RowInfo": RowInfoTypeDef,
        "QueueInfo": QueueInfoTypeDef,
        "IngestionTimeInSeconds": int,
        "IngestionSizeInBytes": int,
        "RequestSource": IngestionRequestSourceType,
        "RequestType": IngestionRequestTypeType,
    },
    total=False,
)


class IngestionTypeDef(_RequiredIngestionTypeDef, _OptionalIngestionTypeDef):
    pass


_RequiredJoinInstructionTypeDef = TypedDict(
    "_RequiredJoinInstructionTypeDef",
    {
        "LeftOperand": str,
        "RightOperand": str,
        "Type": JoinTypeType,
        "OnClause": str,
    },
)
_OptionalJoinInstructionTypeDef = TypedDict(
    "_OptionalJoinInstructionTypeDef",
    {
        "LeftJoinKeyProperties": JoinKeyPropertiesTypeDef,
        "RightJoinKeyProperties": JoinKeyPropertiesTypeDef,
    },
    total=False,
)


class JoinInstructionTypeDef(_RequiredJoinInstructionTypeDef, _OptionalJoinInstructionTypeDef):
    pass


LineChartDefaultSeriesSettingsTypeDef = TypedDict(
    "LineChartDefaultSeriesSettingsTypeDef",
    {
        "AxisBinding": AxisBindingType,
        "LineStyleSettings": LineChartLineStyleSettingsTypeDef,
        "MarkerStyleSettings": LineChartMarkerStyleSettingsTypeDef,
    },
    total=False,
)

LineChartSeriesSettingsTypeDef = TypedDict(
    "LineChartSeriesSettingsTypeDef",
    {
        "LineStyleSettings": LineChartLineStyleSettingsTypeDef,
        "MarkerStyleSettings": LineChartMarkerStyleSettingsTypeDef,
    },
    total=False,
)

_RequiredListAnalysesRequestListAnalysesPaginateTypeDef = TypedDict(
    "_RequiredListAnalysesRequestListAnalysesPaginateTypeDef",
    {
        "AwsAccountId": str,
    },
)
_OptionalListAnalysesRequestListAnalysesPaginateTypeDef = TypedDict(
    "_OptionalListAnalysesRequestListAnalysesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListAnalysesRequestListAnalysesPaginateTypeDef(
    _RequiredListAnalysesRequestListAnalysesPaginateTypeDef,
    _OptionalListAnalysesRequestListAnalysesPaginateTypeDef,
):
    pass


_RequiredListDashboardVersionsRequestListDashboardVersionsPaginateTypeDef = TypedDict(
    "_RequiredListDashboardVersionsRequestListDashboardVersionsPaginateTypeDef",
    {
        "AwsAccountId": str,
        "DashboardId": str,
    },
)
_OptionalListDashboardVersionsRequestListDashboardVersionsPaginateTypeDef = TypedDict(
    "_OptionalListDashboardVersionsRequestListDashboardVersionsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListDashboardVersionsRequestListDashboardVersionsPaginateTypeDef(
    _RequiredListDashboardVersionsRequestListDashboardVersionsPaginateTypeDef,
    _OptionalListDashboardVersionsRequestListDashboardVersionsPaginateTypeDef,
):
    pass


_RequiredListDashboardsRequestListDashboardsPaginateTypeDef = TypedDict(
    "_RequiredListDashboardsRequestListDashboardsPaginateTypeDef",
    {
        "AwsAccountId": str,
    },
)
_OptionalListDashboardsRequestListDashboardsPaginateTypeDef = TypedDict(
    "_OptionalListDashboardsRequestListDashboardsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListDashboardsRequestListDashboardsPaginateTypeDef(
    _RequiredListDashboardsRequestListDashboardsPaginateTypeDef,
    _OptionalListDashboardsRequestListDashboardsPaginateTypeDef,
):
    pass


_RequiredListDataSetsRequestListDataSetsPaginateTypeDef = TypedDict(
    "_RequiredListDataSetsRequestListDataSetsPaginateTypeDef",
    {
        "AwsAccountId": str,
    },
)
_OptionalListDataSetsRequestListDataSetsPaginateTypeDef = TypedDict(
    "_OptionalListDataSetsRequestListDataSetsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListDataSetsRequestListDataSetsPaginateTypeDef(
    _RequiredListDataSetsRequestListDataSetsPaginateTypeDef,
    _OptionalListDataSetsRequestListDataSetsPaginateTypeDef,
):
    pass


_RequiredListDataSourcesRequestListDataSourcesPaginateTypeDef = TypedDict(
    "_RequiredListDataSourcesRequestListDataSourcesPaginateTypeDef",
    {
        "AwsAccountId": str,
    },
)
_OptionalListDataSourcesRequestListDataSourcesPaginateTypeDef = TypedDict(
    "_OptionalListDataSourcesRequestListDataSourcesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListDataSourcesRequestListDataSourcesPaginateTypeDef(
    _RequiredListDataSourcesRequestListDataSourcesPaginateTypeDef,
    _OptionalListDataSourcesRequestListDataSourcesPaginateTypeDef,
):
    pass


_RequiredListIngestionsRequestListIngestionsPaginateTypeDef = TypedDict(
    "_RequiredListIngestionsRequestListIngestionsPaginateTypeDef",
    {
        "DataSetId": str,
        "AwsAccountId": str,
    },
)
_OptionalListIngestionsRequestListIngestionsPaginateTypeDef = TypedDict(
    "_OptionalListIngestionsRequestListIngestionsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListIngestionsRequestListIngestionsPaginateTypeDef(
    _RequiredListIngestionsRequestListIngestionsPaginateTypeDef,
    _OptionalListIngestionsRequestListIngestionsPaginateTypeDef,
):
    pass


_RequiredListNamespacesRequestListNamespacesPaginateTypeDef = TypedDict(
    "_RequiredListNamespacesRequestListNamespacesPaginateTypeDef",
    {
        "AwsAccountId": str,
    },
)
_OptionalListNamespacesRequestListNamespacesPaginateTypeDef = TypedDict(
    "_OptionalListNamespacesRequestListNamespacesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListNamespacesRequestListNamespacesPaginateTypeDef(
    _RequiredListNamespacesRequestListNamespacesPaginateTypeDef,
    _OptionalListNamespacesRequestListNamespacesPaginateTypeDef,
):
    pass


_RequiredListTemplateAliasesRequestListTemplateAliasesPaginateTypeDef = TypedDict(
    "_RequiredListTemplateAliasesRequestListTemplateAliasesPaginateTypeDef",
    {
        "AwsAccountId": str,
        "TemplateId": str,
    },
)
_OptionalListTemplateAliasesRequestListTemplateAliasesPaginateTypeDef = TypedDict(
    "_OptionalListTemplateAliasesRequestListTemplateAliasesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListTemplateAliasesRequestListTemplateAliasesPaginateTypeDef(
    _RequiredListTemplateAliasesRequestListTemplateAliasesPaginateTypeDef,
    _OptionalListTemplateAliasesRequestListTemplateAliasesPaginateTypeDef,
):
    pass


_RequiredListTemplateVersionsRequestListTemplateVersionsPaginateTypeDef = TypedDict(
    "_RequiredListTemplateVersionsRequestListTemplateVersionsPaginateTypeDef",
    {
        "AwsAccountId": str,
        "TemplateId": str,
    },
)
_OptionalListTemplateVersionsRequestListTemplateVersionsPaginateTypeDef = TypedDict(
    "_OptionalListTemplateVersionsRequestListTemplateVersionsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListTemplateVersionsRequestListTemplateVersionsPaginateTypeDef(
    _RequiredListTemplateVersionsRequestListTemplateVersionsPaginateTypeDef,
    _OptionalListTemplateVersionsRequestListTemplateVersionsPaginateTypeDef,
):
    pass


_RequiredListTemplatesRequestListTemplatesPaginateTypeDef = TypedDict(
    "_RequiredListTemplatesRequestListTemplatesPaginateTypeDef",
    {
        "AwsAccountId": str,
    },
)
_OptionalListTemplatesRequestListTemplatesPaginateTypeDef = TypedDict(
    "_OptionalListTemplatesRequestListTemplatesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListTemplatesRequestListTemplatesPaginateTypeDef(
    _RequiredListTemplatesRequestListTemplatesPaginateTypeDef,
    _OptionalListTemplatesRequestListTemplatesPaginateTypeDef,
):
    pass


_RequiredListThemeVersionsRequestListThemeVersionsPaginateTypeDef = TypedDict(
    "_RequiredListThemeVersionsRequestListThemeVersionsPaginateTypeDef",
    {
        "AwsAccountId": str,
        "ThemeId": str,
    },
)
_OptionalListThemeVersionsRequestListThemeVersionsPaginateTypeDef = TypedDict(
    "_OptionalListThemeVersionsRequestListThemeVersionsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListThemeVersionsRequestListThemeVersionsPaginateTypeDef(
    _RequiredListThemeVersionsRequestListThemeVersionsPaginateTypeDef,
    _OptionalListThemeVersionsRequestListThemeVersionsPaginateTypeDef,
):
    pass


_RequiredListThemesRequestListThemesPaginateTypeDef = TypedDict(
    "_RequiredListThemesRequestListThemesPaginateTypeDef",
    {
        "AwsAccountId": str,
    },
)
_OptionalListThemesRequestListThemesPaginateTypeDef = TypedDict(
    "_OptionalListThemesRequestListThemesPaginateTypeDef",
    {
        "Type": ThemeTypeType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListThemesRequestListThemesPaginateTypeDef(
    _RequiredListThemesRequestListThemesPaginateTypeDef,
    _OptionalListThemesRequestListThemesPaginateTypeDef,
):
    pass


_RequiredSearchAnalysesRequestSearchAnalysesPaginateTypeDef = TypedDict(
    "_RequiredSearchAnalysesRequestSearchAnalysesPaginateTypeDef",
    {
        "AwsAccountId": str,
        "Filters": Sequence[AnalysisSearchFilterTypeDef],
    },
)
_OptionalSearchAnalysesRequestSearchAnalysesPaginateTypeDef = TypedDict(
    "_OptionalSearchAnalysesRequestSearchAnalysesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class SearchAnalysesRequestSearchAnalysesPaginateTypeDef(
    _RequiredSearchAnalysesRequestSearchAnalysesPaginateTypeDef,
    _OptionalSearchAnalysesRequestSearchAnalysesPaginateTypeDef,
):
    pass


_RequiredSearchDashboardsRequestSearchDashboardsPaginateTypeDef = TypedDict(
    "_RequiredSearchDashboardsRequestSearchDashboardsPaginateTypeDef",
    {
        "AwsAccountId": str,
        "Filters": Sequence[DashboardSearchFilterTypeDef],
    },
)
_OptionalSearchDashboardsRequestSearchDashboardsPaginateTypeDef = TypedDict(
    "_OptionalSearchDashboardsRequestSearchDashboardsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class SearchDashboardsRequestSearchDashboardsPaginateTypeDef(
    _RequiredSearchDashboardsRequestSearchDashboardsPaginateTypeDef,
    _OptionalSearchDashboardsRequestSearchDashboardsPaginateTypeDef,
):
    pass


_RequiredSearchDataSetsRequestSearchDataSetsPaginateTypeDef = TypedDict(
    "_RequiredSearchDataSetsRequestSearchDataSetsPaginateTypeDef",
    {
        "AwsAccountId": str,
        "Filters": Sequence[DataSetSearchFilterTypeDef],
    },
)
_OptionalSearchDataSetsRequestSearchDataSetsPaginateTypeDef = TypedDict(
    "_OptionalSearchDataSetsRequestSearchDataSetsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class SearchDataSetsRequestSearchDataSetsPaginateTypeDef(
    _RequiredSearchDataSetsRequestSearchDataSetsPaginateTypeDef,
    _OptionalSearchDataSetsRequestSearchDataSetsPaginateTypeDef,
):
    pass


_RequiredSearchDataSourcesRequestSearchDataSourcesPaginateTypeDef = TypedDict(
    "_RequiredSearchDataSourcesRequestSearchDataSourcesPaginateTypeDef",
    {
        "AwsAccountId": str,
        "Filters": Sequence[DataSourceSearchFilterTypeDef],
    },
)
_OptionalSearchDataSourcesRequestSearchDataSourcesPaginateTypeDef = TypedDict(
    "_OptionalSearchDataSourcesRequestSearchDataSourcesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class SearchDataSourcesRequestSearchDataSourcesPaginateTypeDef(
    _RequiredSearchDataSourcesRequestSearchDataSourcesPaginateTypeDef,
    _OptionalSearchDataSourcesRequestSearchDataSourcesPaginateTypeDef,
):
    pass


ListFolderMembersResponseTypeDef = TypedDict(
    "ListFolderMembersResponseTypeDef",
    {
        "Status": int,
        "FolderMemberList": List[MemberIdArnPairTypeDef],
        "NextToken": str,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTemplateVersionsResponseTypeDef = TypedDict(
    "ListTemplateVersionsResponseTypeDef",
    {
        "TemplateVersionSummaryList": List[TemplateVersionSummaryTypeDef],
        "NextToken": str,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTemplatesResponseTypeDef = TypedDict(
    "ListTemplatesResponseTypeDef",
    {
        "TemplateSummaryList": List[TemplateSummaryTypeDef],
        "NextToken": str,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListThemeVersionsResponseTypeDef = TypedDict(
    "ListThemeVersionsResponseTypeDef",
    {
        "ThemeVersionSummaryList": List[ThemeVersionSummaryTypeDef],
        "NextToken": str,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListThemesResponseTypeDef = TypedDict(
    "ListThemesResponseTypeDef",
    {
        "ThemeSummaryList": List[ThemeSummaryTypeDef],
        "NextToken": str,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

VisualSubtitleLabelOptionsTypeDef = TypedDict(
    "VisualSubtitleLabelOptionsTypeDef",
    {
        "Visibility": VisibilityType,
        "FormatText": LongFormatTextTypeDef,
    },
    total=False,
)

_RequiredS3ParametersTypeDef = TypedDict(
    "_RequiredS3ParametersTypeDef",
    {
        "ManifestFileLocation": ManifestFileLocationTypeDef,
    },
)
_OptionalS3ParametersTypeDef = TypedDict(
    "_OptionalS3ParametersTypeDef",
    {
        "RoleArn": str,
    },
    total=False,
)


class S3ParametersTypeDef(_RequiredS3ParametersTypeDef, _OptionalS3ParametersTypeDef):
    pass


TileLayoutStyleTypeDef = TypedDict(
    "TileLayoutStyleTypeDef",
    {
        "Gutter": GutterStyleTypeDef,
        "Margin": MarginStyleTypeDef,
    },
    total=False,
)

NamespaceInfoV2TypeDef = TypedDict(
    "NamespaceInfoV2TypeDef",
    {
        "Name": str,
        "Arn": str,
        "CapacityRegion": str,
        "CreationStatus": NamespaceStatusType,
        "IdentityStore": Literal["QUICKSIGHT"],
        "NamespaceError": NamespaceErrorTypeDef,
    },
    total=False,
)

NumericSeparatorConfigurationTypeDef = TypedDict(
    "NumericSeparatorConfigurationTypeDef",
    {
        "DecimalSeparator": NumericSeparatorSymbolType,
        "ThousandsSeparator": ThousandSeparatorOptionsTypeDef,
    },
    total=False,
)

NumericalAggregationFunctionTypeDef = TypedDict(
    "NumericalAggregationFunctionTypeDef",
    {
        "SimpleNumericalAggregation": SimpleNumericalAggregationFunctionType,
        "PercentileAggregation": PercentileAggregationTypeDef,
    },
    total=False,
)

ParametersTypeDef = TypedDict(
    "ParametersTypeDef",
    {
        "StringParameters": Sequence[StringParameterTypeDef],
        "IntegerParameters": Sequence[IntegerParameterTypeDef],
        "DecimalParameters": Sequence[DecimalParameterTypeDef],
        "DateTimeParameters": Sequence[DateTimeParameterTypeDef],
    },
    total=False,
)

VisibleRangeOptionsTypeDef = TypedDict(
    "VisibleRangeOptionsTypeDef",
    {
        "PercentRange": PercentVisibleRangeTypeDef,
    },
    total=False,
)

RadarChartSeriesSettingsTypeDef = TypedDict(
    "RadarChartSeriesSettingsTypeDef",
    {
        "AreaStyleSettings": RadarChartAreaStyleSettingsTypeDef,
    },
    total=False,
)

_RequiredRefreshFrequencyTypeDef = TypedDict(
    "_RequiredRefreshFrequencyTypeDef",
    {
        "Interval": RefreshIntervalType,
    },
)
_OptionalRefreshFrequencyTypeDef = TypedDict(
    "_OptionalRefreshFrequencyTypeDef",
    {
        "RefreshOnDay": ScheduleRefreshOnEntityTypeDef,
        "Timezone": str,
        "TimeOfTheDay": str,
    },
    total=False,
)


class RefreshFrequencyTypeDef(_RequiredRefreshFrequencyTypeDef, _OptionalRefreshFrequencyTypeDef):
    pass


RegisteredUserConsoleFeatureConfigurationsTypeDef = TypedDict(
    "RegisteredUserConsoleFeatureConfigurationsTypeDef",
    {
        "StatePersistence": StatePersistenceConfigurationsTypeDef,
    },
    total=False,
)

RegisteredUserDashboardFeatureConfigurationsTypeDef = TypedDict(
    "RegisteredUserDashboardFeatureConfigurationsTypeDef",
    {
        "StatePersistence": StatePersistenceConfigurationsTypeDef,
    },
    total=False,
)

_RequiredRowLevelPermissionTagConfigurationTypeDef = TypedDict(
    "_RequiredRowLevelPermissionTagConfigurationTypeDef",
    {
        "TagRules": Sequence[RowLevelPermissionTagRuleTypeDef],
    },
)
_OptionalRowLevelPermissionTagConfigurationTypeDef = TypedDict(
    "_OptionalRowLevelPermissionTagConfigurationTypeDef",
    {
        "Status": StatusType,
        "TagRuleConfigurations": Sequence[Sequence[str]],
    },
    total=False,
)


class RowLevelPermissionTagConfigurationTypeDef(
    _RequiredRowLevelPermissionTagConfigurationTypeDef,
    _OptionalRowLevelPermissionTagConfigurationTypeDef,
):
    pass


_RequiredS3SourceTypeDef = TypedDict(
    "_RequiredS3SourceTypeDef",
    {
        "DataSourceArn": str,
        "InputColumns": Sequence[InputColumnTypeDef],
    },
)
_OptionalS3SourceTypeDef = TypedDict(
    "_OptionalS3SourceTypeDef",
    {
        "UploadSettings": UploadSettingsTypeDef,
    },
    total=False,
)


class S3SourceTypeDef(_RequiredS3SourceTypeDef, _OptionalS3SourceTypeDef):
    pass


SectionPageBreakConfigurationTypeDef = TypedDict(
    "SectionPageBreakConfigurationTypeDef",
    {
        "After": SectionAfterPageBreakTypeDef,
    },
    total=False,
)

SectionBasedLayoutPaperCanvasSizeOptionsTypeDef = TypedDict(
    "SectionBasedLayoutPaperCanvasSizeOptionsTypeDef",
    {
        "PaperSize": PaperSizeType,
        "PaperOrientation": PaperOrientationType,
        "PaperMargin": SpacingTypeDef,
    },
    total=False,
)

SectionStyleTypeDef = TypedDict(
    "SectionStyleTypeDef",
    {
        "Height": str,
        "Padding": SpacingTypeDef,
    },
    total=False,
)

SelectedSheetsFilterScopeConfigurationTypeDef = TypedDict(
    "SelectedSheetsFilterScopeConfigurationTypeDef",
    {
        "SheetVisualScopingConfigurations": Sequence[SheetVisualScopingConfigurationTypeDef],
    },
    total=False,
)

SheetElementRenderingRuleTypeDef = TypedDict(
    "SheetElementRenderingRuleTypeDef",
    {
        "Expression": str,
        "ConfigurationOverrides": SheetElementConfigurationOverridesTypeDef,
    },
)

VisualTitleLabelOptionsTypeDef = TypedDict(
    "VisualTitleLabelOptionsTypeDef",
    {
        "Visibility": VisibilityType,
        "FormatText": ShortFormatTextTypeDef,
    },
    total=False,
)

TableFieldImageConfigurationTypeDef = TypedDict(
    "TableFieldImageConfigurationTypeDef",
    {
        "SizingOptions": TableCellImageSizingConfigurationTypeDef,
    },
    total=False,
)

CascadingControlConfigurationTypeDef = TypedDict(
    "CascadingControlConfigurationTypeDef",
    {
        "SourceControls": Sequence[CascadingControlSourceTypeDef],
    },
    total=False,
)

DateTimeDefaultValuesTypeDef = TypedDict(
    "DateTimeDefaultValuesTypeDef",
    {
        "DynamicValue": DynamicDefaultValueTypeDef,
        "StaticValues": Sequence[Union[datetime, str]],
        "RollingDate": RollingDateConfigurationTypeDef,
    },
    total=False,
)

DecimalDefaultValuesTypeDef = TypedDict(
    "DecimalDefaultValuesTypeDef",
    {
        "DynamicValue": DynamicDefaultValueTypeDef,
        "StaticValues": Sequence[float],
    },
    total=False,
)

IntegerDefaultValuesTypeDef = TypedDict(
    "IntegerDefaultValuesTypeDef",
    {
        "DynamicValue": DynamicDefaultValueTypeDef,
        "StaticValues": Sequence[int],
    },
    total=False,
)

StringDefaultValuesTypeDef = TypedDict(
    "StringDefaultValuesTypeDef",
    {
        "DynamicValue": DynamicDefaultValueTypeDef,
        "StaticValues": Sequence[str],
    },
    total=False,
)

DrillDownFilterTypeDef = TypedDict(
    "DrillDownFilterTypeDef",
    {
        "NumericEqualityFilter": NumericEqualityDrillDownFilterTypeDef,
        "CategoryFilter": CategoryDrillDownFilterTypeDef,
        "TimeRangeFilter": TimeRangeDrillDownFilterTypeDef,
    },
    total=False,
)

AnalysisTypeDef = TypedDict(
    "AnalysisTypeDef",
    {
        "AnalysisId": str,
        "Arn": str,
        "Name": str,
        "Status": ResourceStatusType,
        "Errors": List[AnalysisErrorTypeDef],
        "DataSetArns": List[str],
        "ThemeArn": str,
        "CreatedTime": datetime,
        "LastUpdatedTime": datetime,
        "Sheets": List[SheetTypeDef],
    },
    total=False,
)

DashboardVersionTypeDef = TypedDict(
    "DashboardVersionTypeDef",
    {
        "CreatedTime": datetime,
        "Errors": List[DashboardErrorTypeDef],
        "VersionNumber": int,
        "Status": ResourceStatusType,
        "Arn": str,
        "SourceEntityArn": str,
        "DataSetArns": List[str],
        "Description": str,
        "ThemeArn": str,
        "Sheets": List[SheetTypeDef],
    },
    total=False,
)

AnalysisSourceEntityTypeDef = TypedDict(
    "AnalysisSourceEntityTypeDef",
    {
        "SourceTemplate": AnalysisSourceTemplateTypeDef,
    },
    total=False,
)

DashboardSourceEntityTypeDef = TypedDict(
    "DashboardSourceEntityTypeDef",
    {
        "SourceTemplate": DashboardSourceTemplateTypeDef,
    },
    total=False,
)

TemplateSourceEntityTypeDef = TypedDict(
    "TemplateSourceEntityTypeDef",
    {
        "SourceAnalysis": TemplateSourceAnalysisTypeDef,
        "SourceTemplate": TemplateSourceTemplateTypeDef,
    },
    total=False,
)

AnonymousUserEmbeddingExperienceConfigurationTypeDef = TypedDict(
    "AnonymousUserEmbeddingExperienceConfigurationTypeDef",
    {
        "Dashboard": AnonymousUserDashboardEmbeddingConfigurationTypeDef,
        "DashboardVisual": AnonymousUserDashboardVisualEmbeddingConfigurationTypeDef,
        "QSearchBar": AnonymousUserQSearchBarEmbeddingConfigurationTypeDef,
    },
    total=False,
)

NumericAxisOptionsTypeDef = TypedDict(
    "NumericAxisOptionsTypeDef",
    {
        "Scale": AxisScaleTypeDef,
        "Range": AxisDisplayRangeTypeDef,
    },
    total=False,
)

CategoryFilterTypeDef = TypedDict(
    "CategoryFilterTypeDef",
    {
        "FilterId": str,
        "Column": ColumnIdentifierTypeDef,
        "Configuration": CategoryFilterConfigurationTypeDef,
    },
)

ClusterMarkerConfigurationTypeDef = TypedDict(
    "ClusterMarkerConfigurationTypeDef",
    {
        "ClusterMarker": ClusterMarkerTypeDef,
    },
    total=False,
)

TagColumnOperationTypeDef = TypedDict(
    "TagColumnOperationTypeDef",
    {
        "ColumnName": str,
        "Tags": Sequence[ColumnTagTypeDef],
    },
)

DataSetConfigurationTypeDef = TypedDict(
    "DataSetConfigurationTypeDef",
    {
        "Placeholder": str,
        "DataSetSchema": DataSetSchemaTypeDef,
        "ColumnGroupSchemaList": Sequence[ColumnGroupSchemaTypeDef],
    },
    total=False,
)

ConditionalFormattingIconTypeDef = TypedDict(
    "ConditionalFormattingIconTypeDef",
    {
        "IconSet": ConditionalFormattingIconSetTypeDef,
        "CustomCondition": ConditionalFormattingCustomIconConditionTypeDef,
    },
    total=False,
)

DescribeDashboardPermissionsResponseTypeDef = TypedDict(
    "DescribeDashboardPermissionsResponseTypeDef",
    {
        "DashboardId": str,
        "DashboardArn": str,
        "Permissions": List[ResourcePermissionTypeDef],
        "Status": int,
        "RequestId": str,
        "LinkSharingConfiguration": LinkSharingConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateDashboardPermissionsResponseTypeDef = TypedDict(
    "UpdateDashboardPermissionsResponseTypeDef",
    {
        "DashboardArn": str,
        "DashboardId": str,
        "Permissions": List[ResourcePermissionTypeDef],
        "RequestId": str,
        "Status": int,
        "LinkSharingConfiguration": LinkSharingConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListDataSetsResponseTypeDef = TypedDict(
    "ListDataSetsResponseTypeDef",
    {
        "DataSetSummaries": List[DataSetSummaryTypeDef],
        "NextToken": str,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SearchDataSetsResponseTypeDef = TypedDict(
    "SearchDataSetsResponseTypeDef",
    {
        "DataSetSummaries": List[DataSetSummaryTypeDef],
        "NextToken": str,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DestinationParameterValueConfigurationTypeDef = TypedDict(
    "DestinationParameterValueConfigurationTypeDef",
    {
        "CustomValuesConfiguration": CustomValuesConfigurationTypeDef,
        "SelectAllValueOptions": Literal["ALL_VALUES"],
        "SourceParameterName": str,
        "SourceField": str,
    },
    total=False,
)

DashboardPublishOptionsTypeDef = TypedDict(
    "DashboardPublishOptionsTypeDef",
    {
        "AdHocFilteringOption": AdHocFilteringOptionTypeDef,
        "ExportToCSVOption": ExportToCSVOptionTypeDef,
        "SheetControlsOption": SheetControlsOptionTypeDef,
        "VisualPublishOptions": DashboardVisualPublishOptionsTypeDef,
        "SheetLayoutElementMaximizationOption": SheetLayoutElementMaximizationOptionTypeDef,
        "VisualMenuOption": VisualMenuOptionTypeDef,
        "VisualAxisSortOption": VisualAxisSortOptionTypeDef,
        "ExportWithHiddenFieldsOption": ExportWithHiddenFieldsOptionTypeDef,
        "DataPointDrillUpDownOption": DataPointDrillUpDownOptionTypeDef,
        "DataPointMenuLabelOption": DataPointMenuLabelOptionTypeDef,
        "DataPointTooltipOption": DataPointTooltipOptionTypeDef,
    },
    total=False,
)

VisualPaletteTypeDef = TypedDict(
    "VisualPaletteTypeDef",
    {
        "ChartColor": str,
        "ColorMap": Sequence[DataPathColorTypeDef],
    },
    total=False,
)

PivotTableFieldOptionsTypeDef = TypedDict(
    "PivotTableFieldOptionsTypeDef",
    {
        "SelectedFieldOptions": Sequence[PivotTableFieldOptionTypeDef],
        "DataPathOptions": Sequence[PivotTableDataPathOptionTypeDef],
    },
    total=False,
)

_RequiredTimeRangeFilterTypeDef = TypedDict(
    "_RequiredTimeRangeFilterTypeDef",
    {
        "FilterId": str,
        "Column": ColumnIdentifierTypeDef,
        "NullOption": FilterNullOptionType,
    },
)
_OptionalTimeRangeFilterTypeDef = TypedDict(
    "_OptionalTimeRangeFilterTypeDef",
    {
        "IncludeMinimum": bool,
        "IncludeMaximum": bool,
        "RangeMinimumValue": TimeRangeFilterValueTypeDef,
        "RangeMaximumValue": TimeRangeFilterValueTypeDef,
        "ExcludePeriodConfiguration": ExcludePeriodConfigurationTypeDef,
        "TimeGranularity": TimeGranularityType,
    },
    total=False,
)


class TimeRangeFilterTypeDef(_RequiredTimeRangeFilterTypeDef, _OptionalTimeRangeFilterTypeDef):
    pass


CustomActionFilterOperationTypeDef = TypedDict(
    "CustomActionFilterOperationTypeDef",
    {
        "SelectedFieldsConfiguration": FilterOperationSelectedFieldsConfigurationTypeDef,
        "TargetVisualsConfiguration": FilterOperationTargetVisualsConfigurationTypeDef,
    },
)

AxisLabelOptionsTypeDef = TypedDict(
    "AxisLabelOptionsTypeDef",
    {
        "FontConfiguration": FontConfigurationTypeDef,
        "CustomLabel": str,
        "ApplyTo": AxisLabelReferenceOptionsTypeDef,
    },
    total=False,
)

DataLabelOptionsTypeDef = TypedDict(
    "DataLabelOptionsTypeDef",
    {
        "Visibility": VisibilityType,
        "CategoryLabelVisibility": VisibilityType,
        "MeasureLabelVisibility": VisibilityType,
        "DataLabelTypes": Sequence[DataLabelTypeTypeDef],
        "Position": DataLabelPositionType,
        "LabelContent": DataLabelContentType,
        "LabelFontConfiguration": FontConfigurationTypeDef,
        "LabelColor": str,
        "Overlap": DataLabelOverlapType,
    },
    total=False,
)

FunnelChartDataLabelOptionsTypeDef = TypedDict(
    "FunnelChartDataLabelOptionsTypeDef",
    {
        "Visibility": VisibilityType,
        "CategoryLabelVisibility": VisibilityType,
        "MeasureLabelVisibility": VisibilityType,
        "Position": DataLabelPositionType,
        "LabelFontConfiguration": FontConfigurationTypeDef,
        "LabelColor": str,
        "MeasureDataLabelStyle": FunnelChartMeasureDataLabelStyleType,
    },
    total=False,
)

LabelOptionsTypeDef = TypedDict(
    "LabelOptionsTypeDef",
    {
        "Visibility": VisibilityType,
        "FontConfiguration": FontConfigurationTypeDef,
        "CustomLabel": str,
    },
    total=False,
)

PanelTitleOptionsTypeDef = TypedDict(
    "PanelTitleOptionsTypeDef",
    {
        "Visibility": VisibilityType,
        "FontConfiguration": FontConfigurationTypeDef,
        "HorizontalTextAlignment": HorizontalTextAlignmentType,
    },
    total=False,
)

_RequiredTableFieldCustomTextContentTypeDef = TypedDict(
    "_RequiredTableFieldCustomTextContentTypeDef",
    {
        "FontConfiguration": FontConfigurationTypeDef,
    },
)
_OptionalTableFieldCustomTextContentTypeDef = TypedDict(
    "_OptionalTableFieldCustomTextContentTypeDef",
    {
        "Value": str,
    },
    total=False,
)


class TableFieldCustomTextContentTypeDef(
    _RequiredTableFieldCustomTextContentTypeDef, _OptionalTableFieldCustomTextContentTypeDef
):
    pass


ForecastConfigurationTypeDef = TypedDict(
    "ForecastConfigurationTypeDef",
    {
        "ForecastProperties": TimeBasedForecastPropertiesTypeDef,
        "Scenario": ForecastScenarioTypeDef,
    },
    total=False,
)

DefaultFreeFormLayoutConfigurationTypeDef = TypedDict(
    "DefaultFreeFormLayoutConfigurationTypeDef",
    {
        "CanvasSizeOptions": FreeFormLayoutCanvasSizeOptionsTypeDef,
    },
)

GlobalTableBorderOptionsTypeDef = TypedDict(
    "GlobalTableBorderOptionsTypeDef",
    {
        "UniformBorder": TableBorderOptionsTypeDef,
        "SideSpecificBorder": TableSideBorderOptionsTypeDef,
    },
    total=False,
)

ConditionalFormattingGradientColorTypeDef = TypedDict(
    "ConditionalFormattingGradientColorTypeDef",
    {
        "Expression": str,
        "Color": GradientColorTypeDef,
    },
)

DefaultGridLayoutConfigurationTypeDef = TypedDict(
    "DefaultGridLayoutConfigurationTypeDef",
    {
        "CanvasSizeOptions": GridLayoutCanvasSizeOptionsTypeDef,
    },
)

_RequiredGridLayoutConfigurationTypeDef = TypedDict(
    "_RequiredGridLayoutConfigurationTypeDef",
    {
        "Elements": Sequence[GridLayoutElementTypeDef],
    },
)
_OptionalGridLayoutConfigurationTypeDef = TypedDict(
    "_OptionalGridLayoutConfigurationTypeDef",
    {
        "CanvasSizeOptions": GridLayoutCanvasSizeOptionsTypeDef,
    },
    total=False,
)


class GridLayoutConfigurationTypeDef(
    _RequiredGridLayoutConfigurationTypeDef, _OptionalGridLayoutConfigurationTypeDef
):
    pass


RefreshConfigurationTypeDef = TypedDict(
    "RefreshConfigurationTypeDef",
    {
        "IncrementalRefresh": IncrementalRefreshTypeDef,
    },
)

DescribeIngestionResponseTypeDef = TypedDict(
    "DescribeIngestionResponseTypeDef",
    {
        "Ingestion": IngestionTypeDef,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListIngestionsResponseTypeDef = TypedDict(
    "ListIngestionsResponseTypeDef",
    {
        "Ingestions": List[IngestionTypeDef],
        "NextToken": str,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

LogicalTableSourceTypeDef = TypedDict(
    "LogicalTableSourceTypeDef",
    {
        "JoinInstruction": JoinInstructionTypeDef,
        "PhysicalTableId": str,
        "DataSetArn": str,
    },
    total=False,
)

_RequiredDataFieldSeriesItemTypeDef = TypedDict(
    "_RequiredDataFieldSeriesItemTypeDef",
    {
        "FieldId": str,
        "AxisBinding": AxisBindingType,
    },
)
_OptionalDataFieldSeriesItemTypeDef = TypedDict(
    "_OptionalDataFieldSeriesItemTypeDef",
    {
        "FieldValue": str,
        "Settings": LineChartSeriesSettingsTypeDef,
    },
    total=False,
)


class DataFieldSeriesItemTypeDef(
    _RequiredDataFieldSeriesItemTypeDef, _OptionalDataFieldSeriesItemTypeDef
):
    pass


_RequiredFieldSeriesItemTypeDef = TypedDict(
    "_RequiredFieldSeriesItemTypeDef",
    {
        "FieldId": str,
        "AxisBinding": AxisBindingType,
    },
)
_OptionalFieldSeriesItemTypeDef = TypedDict(
    "_OptionalFieldSeriesItemTypeDef",
    {
        "Settings": LineChartSeriesSettingsTypeDef,
    },
    total=False,
)


class FieldSeriesItemTypeDef(_RequiredFieldSeriesItemTypeDef, _OptionalFieldSeriesItemTypeDef):
    pass


DataSourceParametersTypeDef = TypedDict(
    "DataSourceParametersTypeDef",
    {
        "AmazonElasticsearchParameters": AmazonElasticsearchParametersTypeDef,
        "AthenaParameters": AthenaParametersTypeDef,
        "AuroraParameters": AuroraParametersTypeDef,
        "AuroraPostgreSqlParameters": AuroraPostgreSqlParametersTypeDef,
        "AwsIotAnalyticsParameters": AwsIotAnalyticsParametersTypeDef,
        "JiraParameters": JiraParametersTypeDef,
        "MariaDbParameters": MariaDbParametersTypeDef,
        "MySqlParameters": MySqlParametersTypeDef,
        "OracleParameters": OracleParametersTypeDef,
        "PostgreSqlParameters": PostgreSqlParametersTypeDef,
        "PrestoParameters": PrestoParametersTypeDef,
        "RdsParameters": RdsParametersTypeDef,
        "RedshiftParameters": RedshiftParametersTypeDef,
        "S3Parameters": S3ParametersTypeDef,
        "ServiceNowParameters": ServiceNowParametersTypeDef,
        "SnowflakeParameters": SnowflakeParametersTypeDef,
        "SparkParameters": SparkParametersTypeDef,
        "SqlServerParameters": SqlServerParametersTypeDef,
        "TeradataParameters": TeradataParametersTypeDef,
        "TwitterParameters": TwitterParametersTypeDef,
        "AmazonOpenSearchParameters": AmazonOpenSearchParametersTypeDef,
        "ExasolParameters": ExasolParametersTypeDef,
        "DatabricksParameters": DatabricksParametersTypeDef,
    },
    total=False,
)

SheetStyleTypeDef = TypedDict(
    "SheetStyleTypeDef",
    {
        "Tile": TileStyleTypeDef,
        "TileLayout": TileLayoutStyleTypeDef,
    },
    total=False,
)

DescribeNamespaceResponseTypeDef = TypedDict(
    "DescribeNamespaceResponseTypeDef",
    {
        "Namespace": NamespaceInfoV2TypeDef,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListNamespacesResponseTypeDef = TypedDict(
    "ListNamespacesResponseTypeDef",
    {
        "Namespaces": List[NamespaceInfoV2TypeDef],
        "NextToken": str,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CurrencyDisplayFormatConfigurationTypeDef = TypedDict(
    "CurrencyDisplayFormatConfigurationTypeDef",
    {
        "Prefix": str,
        "Suffix": str,
        "SeparatorConfiguration": NumericSeparatorConfigurationTypeDef,
        "Symbol": str,
        "DecimalPlacesConfiguration": DecimalPlacesConfigurationTypeDef,
        "NumberScale": NumberScaleType,
        "NegativeValueConfiguration": NegativeValueConfigurationTypeDef,
        "NullValueFormatConfiguration": NullValueFormatConfigurationTypeDef,
    },
    total=False,
)

NumberDisplayFormatConfigurationTypeDef = TypedDict(
    "NumberDisplayFormatConfigurationTypeDef",
    {
        "Prefix": str,
        "Suffix": str,
        "SeparatorConfiguration": NumericSeparatorConfigurationTypeDef,
        "DecimalPlacesConfiguration": DecimalPlacesConfigurationTypeDef,
        "NumberScale": NumberScaleType,
        "NegativeValueConfiguration": NegativeValueConfigurationTypeDef,
        "NullValueFormatConfiguration": NullValueFormatConfigurationTypeDef,
    },
    total=False,
)

PercentageDisplayFormatConfigurationTypeDef = TypedDict(
    "PercentageDisplayFormatConfigurationTypeDef",
    {
        "Prefix": str,
        "Suffix": str,
        "SeparatorConfiguration": NumericSeparatorConfigurationTypeDef,
        "DecimalPlacesConfiguration": DecimalPlacesConfigurationTypeDef,
        "NegativeValueConfiguration": NegativeValueConfigurationTypeDef,
        "NullValueFormatConfiguration": NullValueFormatConfigurationTypeDef,
    },
    total=False,
)

AggregationFunctionTypeDef = TypedDict(
    "AggregationFunctionTypeDef",
    {
        "NumericalAggregationFunction": NumericalAggregationFunctionTypeDef,
        "CategoricalAggregationFunction": CategoricalAggregationFunctionType,
        "DateAggregationFunction": DateAggregationFunctionType,
    },
    total=False,
)

ScrollBarOptionsTypeDef = TypedDict(
    "ScrollBarOptionsTypeDef",
    {
        "Visibility": VisibilityType,
        "VisibleRange": VisibleRangeOptionsTypeDef,
    },
    total=False,
)

_RequiredRefreshScheduleTypeDef = TypedDict(
    "_RequiredRefreshScheduleTypeDef",
    {
        "ScheduleId": str,
        "ScheduleFrequency": RefreshFrequencyTypeDef,
        "RefreshType": IngestionTypeType,
    },
)
_OptionalRefreshScheduleTypeDef = TypedDict(
    "_OptionalRefreshScheduleTypeDef",
    {
        "StartAfterDateTime": Union[datetime, str],
        "Arn": str,
    },
    total=False,
)


class RefreshScheduleTypeDef(_RequiredRefreshScheduleTypeDef, _OptionalRefreshScheduleTypeDef):
    pass


RegisteredUserQuickSightConsoleEmbeddingConfigurationTypeDef = TypedDict(
    "RegisteredUserQuickSightConsoleEmbeddingConfigurationTypeDef",
    {
        "InitialPath": str,
        "FeatureConfigurations": RegisteredUserConsoleFeatureConfigurationsTypeDef,
    },
    total=False,
)

_RequiredRegisteredUserDashboardEmbeddingConfigurationTypeDef = TypedDict(
    "_RequiredRegisteredUserDashboardEmbeddingConfigurationTypeDef",
    {
        "InitialDashboardId": str,
    },
)
_OptionalRegisteredUserDashboardEmbeddingConfigurationTypeDef = TypedDict(
    "_OptionalRegisteredUserDashboardEmbeddingConfigurationTypeDef",
    {
        "FeatureConfigurations": RegisteredUserDashboardFeatureConfigurationsTypeDef,
    },
    total=False,
)


class RegisteredUserDashboardEmbeddingConfigurationTypeDef(
    _RequiredRegisteredUserDashboardEmbeddingConfigurationTypeDef,
    _OptionalRegisteredUserDashboardEmbeddingConfigurationTypeDef,
):
    pass


PhysicalTableTypeDef = TypedDict(
    "PhysicalTableTypeDef",
    {
        "RelationalTable": RelationalTableTypeDef,
        "CustomSql": CustomSqlTypeDef,
        "S3Source": S3SourceTypeDef,
    },
    total=False,
)

SectionBasedLayoutCanvasSizeOptionsTypeDef = TypedDict(
    "SectionBasedLayoutCanvasSizeOptionsTypeDef",
    {
        "PaperCanvasSizeOptions": SectionBasedLayoutPaperCanvasSizeOptionsTypeDef,
    },
    total=False,
)

FilterScopeConfigurationTypeDef = TypedDict(
    "FilterScopeConfigurationTypeDef",
    {
        "SelectedSheets": SelectedSheetsFilterScopeConfigurationTypeDef,
    },
    total=False,
)

_RequiredFreeFormLayoutElementTypeDef = TypedDict(
    "_RequiredFreeFormLayoutElementTypeDef",
    {
        "ElementId": str,
        "ElementType": LayoutElementTypeType,
        "XAxisLocation": str,
        "YAxisLocation": str,
        "Width": str,
        "Height": str,
    },
)
_OptionalFreeFormLayoutElementTypeDef = TypedDict(
    "_OptionalFreeFormLayoutElementTypeDef",
    {
        "Visibility": VisibilityType,
        "RenderingRules": Sequence[SheetElementRenderingRuleTypeDef],
        "BorderStyle": FreeFormLayoutElementBorderStyleTypeDef,
        "SelectedBorderStyle": FreeFormLayoutElementBorderStyleTypeDef,
        "BackgroundStyle": FreeFormLayoutElementBackgroundStyleTypeDef,
        "LoadingAnimation": LoadingAnimationTypeDef,
    },
    total=False,
)


class FreeFormLayoutElementTypeDef(
    _RequiredFreeFormLayoutElementTypeDef, _OptionalFreeFormLayoutElementTypeDef
):
    pass


_RequiredDateTimeParameterDeclarationTypeDef = TypedDict(
    "_RequiredDateTimeParameterDeclarationTypeDef",
    {
        "Name": str,
    },
)
_OptionalDateTimeParameterDeclarationTypeDef = TypedDict(
    "_OptionalDateTimeParameterDeclarationTypeDef",
    {
        "DefaultValues": DateTimeDefaultValuesTypeDef,
        "TimeGranularity": TimeGranularityType,
        "ValueWhenUnset": DateTimeValueWhenUnsetConfigurationTypeDef,
    },
    total=False,
)


class DateTimeParameterDeclarationTypeDef(
    _RequiredDateTimeParameterDeclarationTypeDef, _OptionalDateTimeParameterDeclarationTypeDef
):
    pass


_RequiredDecimalParameterDeclarationTypeDef = TypedDict(
    "_RequiredDecimalParameterDeclarationTypeDef",
    {
        "ParameterValueType": ParameterValueTypeType,
        "Name": str,
    },
)
_OptionalDecimalParameterDeclarationTypeDef = TypedDict(
    "_OptionalDecimalParameterDeclarationTypeDef",
    {
        "DefaultValues": DecimalDefaultValuesTypeDef,
        "ValueWhenUnset": DecimalValueWhenUnsetConfigurationTypeDef,
    },
    total=False,
)


class DecimalParameterDeclarationTypeDef(
    _RequiredDecimalParameterDeclarationTypeDef, _OptionalDecimalParameterDeclarationTypeDef
):
    pass


_RequiredIntegerParameterDeclarationTypeDef = TypedDict(
    "_RequiredIntegerParameterDeclarationTypeDef",
    {
        "ParameterValueType": ParameterValueTypeType,
        "Name": str,
    },
)
_OptionalIntegerParameterDeclarationTypeDef = TypedDict(
    "_OptionalIntegerParameterDeclarationTypeDef",
    {
        "DefaultValues": IntegerDefaultValuesTypeDef,
        "ValueWhenUnset": IntegerValueWhenUnsetConfigurationTypeDef,
    },
    total=False,
)


class IntegerParameterDeclarationTypeDef(
    _RequiredIntegerParameterDeclarationTypeDef, _OptionalIntegerParameterDeclarationTypeDef
):
    pass


_RequiredStringParameterDeclarationTypeDef = TypedDict(
    "_RequiredStringParameterDeclarationTypeDef",
    {
        "ParameterValueType": ParameterValueTypeType,
        "Name": str,
    },
)
_OptionalStringParameterDeclarationTypeDef = TypedDict(
    "_OptionalStringParameterDeclarationTypeDef",
    {
        "DefaultValues": StringDefaultValuesTypeDef,
        "ValueWhenUnset": StringValueWhenUnsetConfigurationTypeDef,
    },
    total=False,
)


class StringParameterDeclarationTypeDef(
    _RequiredStringParameterDeclarationTypeDef, _OptionalStringParameterDeclarationTypeDef
):
    pass


_RequiredDateTimeHierarchyTypeDef = TypedDict(
    "_RequiredDateTimeHierarchyTypeDef",
    {
        "HierarchyId": str,
    },
)
_OptionalDateTimeHierarchyTypeDef = TypedDict(
    "_OptionalDateTimeHierarchyTypeDef",
    {
        "DrillDownFilters": Sequence[DrillDownFilterTypeDef],
    },
    total=False,
)


class DateTimeHierarchyTypeDef(
    _RequiredDateTimeHierarchyTypeDef, _OptionalDateTimeHierarchyTypeDef
):
    pass


_RequiredExplicitHierarchyTypeDef = TypedDict(
    "_RequiredExplicitHierarchyTypeDef",
    {
        "HierarchyId": str,
        "Columns": Sequence[ColumnIdentifierTypeDef],
    },
)
_OptionalExplicitHierarchyTypeDef = TypedDict(
    "_OptionalExplicitHierarchyTypeDef",
    {
        "DrillDownFilters": Sequence[DrillDownFilterTypeDef],
    },
    total=False,
)


class ExplicitHierarchyTypeDef(
    _RequiredExplicitHierarchyTypeDef, _OptionalExplicitHierarchyTypeDef
):
    pass


_RequiredPredefinedHierarchyTypeDef = TypedDict(
    "_RequiredPredefinedHierarchyTypeDef",
    {
        "HierarchyId": str,
        "Columns": Sequence[ColumnIdentifierTypeDef],
    },
)
_OptionalPredefinedHierarchyTypeDef = TypedDict(
    "_OptionalPredefinedHierarchyTypeDef",
    {
        "DrillDownFilters": Sequence[DrillDownFilterTypeDef],
    },
    total=False,
)


class PredefinedHierarchyTypeDef(
    _RequiredPredefinedHierarchyTypeDef, _OptionalPredefinedHierarchyTypeDef
):
    pass


DescribeAnalysisResponseTypeDef = TypedDict(
    "DescribeAnalysisResponseTypeDef",
    {
        "Analysis": AnalysisTypeDef,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DashboardTypeDef = TypedDict(
    "DashboardTypeDef",
    {
        "DashboardId": str,
        "Arn": str,
        "Name": str,
        "Version": DashboardVersionTypeDef,
        "CreatedTime": datetime,
        "LastPublishedTime": datetime,
        "LastUpdatedTime": datetime,
    },
    total=False,
)

_RequiredGenerateEmbedUrlForAnonymousUserRequestRequestTypeDef = TypedDict(
    "_RequiredGenerateEmbedUrlForAnonymousUserRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "Namespace": str,
        "AuthorizedResourceArns": Sequence[str],
        "ExperienceConfiguration": AnonymousUserEmbeddingExperienceConfigurationTypeDef,
    },
)
_OptionalGenerateEmbedUrlForAnonymousUserRequestRequestTypeDef = TypedDict(
    "_OptionalGenerateEmbedUrlForAnonymousUserRequestRequestTypeDef",
    {
        "SessionLifetimeInMinutes": int,
        "SessionTags": Sequence[SessionTagTypeDef],
        "AllowedDomains": Sequence[str],
    },
    total=False,
)


class GenerateEmbedUrlForAnonymousUserRequestRequestTypeDef(
    _RequiredGenerateEmbedUrlForAnonymousUserRequestRequestTypeDef,
    _OptionalGenerateEmbedUrlForAnonymousUserRequestRequestTypeDef,
):
    pass


AxisDataOptionsTypeDef = TypedDict(
    "AxisDataOptionsTypeDef",
    {
        "NumericAxisOptions": NumericAxisOptionsTypeDef,
        "DateAxisOptions": DateAxisOptionsTypeDef,
    },
    total=False,
)

GeospatialPointStyleOptionsTypeDef = TypedDict(
    "GeospatialPointStyleOptionsTypeDef",
    {
        "SelectedPointStyle": GeospatialSelectedPointStyleType,
        "ClusterMarkerConfiguration": ClusterMarkerConfigurationTypeDef,
    },
    total=False,
)

TransformOperationTypeDef = TypedDict(
    "TransformOperationTypeDef",
    {
        "ProjectOperation": ProjectOperationTypeDef,
        "FilterOperation": FilterOperationTypeDef,
        "CreateColumnsOperation": CreateColumnsOperationTypeDef,
        "RenameColumnOperation": RenameColumnOperationTypeDef,
        "CastColumnTypeOperation": CastColumnTypeOperationTypeDef,
        "TagColumnOperation": TagColumnOperationTypeDef,
        "UntagColumnOperation": UntagColumnOperationTypeDef,
    },
    total=False,
)

TemplateVersionTypeDef = TypedDict(
    "TemplateVersionTypeDef",
    {
        "CreatedTime": datetime,
        "Errors": List[TemplateErrorTypeDef],
        "VersionNumber": int,
        "Status": ResourceStatusType,
        "DataSetConfigurations": List[DataSetConfigurationTypeDef],
        "Description": str,
        "SourceEntityArn": str,
        "ThemeArn": str,
        "Sheets": List[SheetTypeDef],
    },
    total=False,
)

SetParameterValueConfigurationTypeDef = TypedDict(
    "SetParameterValueConfigurationTypeDef",
    {
        "DestinationParameterName": str,
        "Value": DestinationParameterValueConfigurationTypeDef,
    },
)

ChartAxisLabelOptionsTypeDef = TypedDict(
    "ChartAxisLabelOptionsTypeDef",
    {
        "Visibility": VisibilityType,
        "SortIconVisibility": VisibilityType,
        "AxisLabelOptions": Sequence[AxisLabelOptionsTypeDef],
    },
    total=False,
)

AxisTickLabelOptionsTypeDef = TypedDict(
    "AxisTickLabelOptionsTypeDef",
    {
        "LabelOptions": LabelOptionsTypeDef,
        "RotationAngle": float,
    },
    total=False,
)

DateTimePickerControlDisplayOptionsTypeDef = TypedDict(
    "DateTimePickerControlDisplayOptionsTypeDef",
    {
        "TitleOptions": LabelOptionsTypeDef,
        "DateTimeFormat": str,
    },
    total=False,
)

DropDownControlDisplayOptionsTypeDef = TypedDict(
    "DropDownControlDisplayOptionsTypeDef",
    {
        "SelectAllOptions": ListControlSelectAllOptionsTypeDef,
        "TitleOptions": LabelOptionsTypeDef,
    },
    total=False,
)

LegendOptionsTypeDef = TypedDict(
    "LegendOptionsTypeDef",
    {
        "Visibility": VisibilityType,
        "Title": LabelOptionsTypeDef,
        "Position": LegendPositionType,
        "Width": str,
        "Height": str,
    },
    total=False,
)

ListControlDisplayOptionsTypeDef = TypedDict(
    "ListControlDisplayOptionsTypeDef",
    {
        "SearchOptions": ListControlSearchOptionsTypeDef,
        "SelectAllOptions": ListControlSelectAllOptionsTypeDef,
        "TitleOptions": LabelOptionsTypeDef,
    },
    total=False,
)

RelativeDateTimeControlDisplayOptionsTypeDef = TypedDict(
    "RelativeDateTimeControlDisplayOptionsTypeDef",
    {
        "TitleOptions": LabelOptionsTypeDef,
        "DateTimeFormat": str,
    },
    total=False,
)

SliderControlDisplayOptionsTypeDef = TypedDict(
    "SliderControlDisplayOptionsTypeDef",
    {
        "TitleOptions": LabelOptionsTypeDef,
    },
    total=False,
)

TextAreaControlDisplayOptionsTypeDef = TypedDict(
    "TextAreaControlDisplayOptionsTypeDef",
    {
        "TitleOptions": LabelOptionsTypeDef,
        "PlaceholderOptions": TextControlPlaceholderOptionsTypeDef,
    },
    total=False,
)

TextFieldControlDisplayOptionsTypeDef = TypedDict(
    "TextFieldControlDisplayOptionsTypeDef",
    {
        "TitleOptions": LabelOptionsTypeDef,
        "PlaceholderOptions": TextControlPlaceholderOptionsTypeDef,
    },
    total=False,
)

PanelConfigurationTypeDef = TypedDict(
    "PanelConfigurationTypeDef",
    {
        "Title": PanelTitleOptionsTypeDef,
        "BorderVisibility": VisibilityType,
        "BorderThickness": str,
        "BorderStyle": PanelBorderStyleType,
        "BorderColor": str,
        "GutterVisibility": VisibilityType,
        "GutterSpacing": str,
        "BackgroundVisibility": VisibilityType,
        "BackgroundColor": str,
    },
    total=False,
)

TableFieldLinkContentConfigurationTypeDef = TypedDict(
    "TableFieldLinkContentConfigurationTypeDef",
    {
        "CustomTextContent": TableFieldCustomTextContentTypeDef,
        "CustomIconContent": TableFieldCustomIconContentTypeDef,
    },
    total=False,
)

TableCellStyleTypeDef = TypedDict(
    "TableCellStyleTypeDef",
    {
        "Visibility": VisibilityType,
        "FontConfiguration": FontConfigurationTypeDef,
        "TextWrap": TextWrapType,
        "HorizontalTextAlignment": HorizontalTextAlignmentType,
        "VerticalTextAlignment": VerticalTextAlignmentType,
        "BackgroundColor": str,
        "Height": int,
        "Border": GlobalTableBorderOptionsTypeDef,
    },
    total=False,
)

ConditionalFormattingColorTypeDef = TypedDict(
    "ConditionalFormattingColorTypeDef",
    {
        "Solid": ConditionalFormattingSolidColorTypeDef,
        "Gradient": ConditionalFormattingGradientColorTypeDef,
    },
    total=False,
)

DefaultInteractiveLayoutConfigurationTypeDef = TypedDict(
    "DefaultInteractiveLayoutConfigurationTypeDef",
    {
        "Grid": DefaultGridLayoutConfigurationTypeDef,
        "FreeForm": DefaultFreeFormLayoutConfigurationTypeDef,
    },
    total=False,
)

SheetControlLayoutConfigurationTypeDef = TypedDict(
    "SheetControlLayoutConfigurationTypeDef",
    {
        "GridLayout": GridLayoutConfigurationTypeDef,
    },
    total=False,
)

DataSetRefreshPropertiesTypeDef = TypedDict(
    "DataSetRefreshPropertiesTypeDef",
    {
        "RefreshConfiguration": RefreshConfigurationTypeDef,
    },
)

SeriesItemTypeDef = TypedDict(
    "SeriesItemTypeDef",
    {
        "FieldSeriesItem": FieldSeriesItemTypeDef,
        "DataFieldSeriesItem": DataFieldSeriesItemTypeDef,
    },
    total=False,
)

_RequiredCredentialPairTypeDef = TypedDict(
    "_RequiredCredentialPairTypeDef",
    {
        "Username": str,
        "Password": str,
    },
)
_OptionalCredentialPairTypeDef = TypedDict(
    "_OptionalCredentialPairTypeDef",
    {
        "AlternateDataSourceParameters": Sequence[DataSourceParametersTypeDef],
    },
    total=False,
)


class CredentialPairTypeDef(_RequiredCredentialPairTypeDef, _OptionalCredentialPairTypeDef):
    pass


DataSourceTypeDef = TypedDict(
    "DataSourceTypeDef",
    {
        "Arn": str,
        "DataSourceId": str,
        "Name": str,
        "Type": DataSourceTypeType,
        "Status": ResourceStatusType,
        "CreatedTime": datetime,
        "LastUpdatedTime": datetime,
        "DataSourceParameters": DataSourceParametersTypeDef,
        "AlternateDataSourceParameters": List[DataSourceParametersTypeDef],
        "VpcConnectionProperties": VpcConnectionPropertiesTypeDef,
        "SslProperties": SslPropertiesTypeDef,
        "ErrorInfo": DataSourceErrorInfoTypeDef,
        "SecretArn": str,
    },
    total=False,
)

ThemeConfigurationTypeDef = TypedDict(
    "ThemeConfigurationTypeDef",
    {
        "DataColorPalette": DataColorPaletteTypeDef,
        "UIColorPalette": UIColorPaletteTypeDef,
        "Sheet": SheetStyleTypeDef,
        "Typography": TypographyTypeDef,
    },
    total=False,
)

ComparisonFormatConfigurationTypeDef = TypedDict(
    "ComparisonFormatConfigurationTypeDef",
    {
        "NumberDisplayFormatConfiguration": NumberDisplayFormatConfigurationTypeDef,
        "PercentageDisplayFormatConfiguration": PercentageDisplayFormatConfigurationTypeDef,
    },
    total=False,
)

NumericFormatConfigurationTypeDef = TypedDict(
    "NumericFormatConfigurationTypeDef",
    {
        "NumberDisplayFormatConfiguration": NumberDisplayFormatConfigurationTypeDef,
        "CurrencyDisplayFormatConfiguration": CurrencyDisplayFormatConfigurationTypeDef,
        "PercentageDisplayFormatConfiguration": PercentageDisplayFormatConfigurationTypeDef,
    },
    total=False,
)

AggregationSortConfigurationTypeDef = TypedDict(
    "AggregationSortConfigurationTypeDef",
    {
        "Column": ColumnIdentifierTypeDef,
        "SortDirection": SortDirectionType,
        "AggregationFunction": AggregationFunctionTypeDef,
    },
)

_RequiredColumnSortTypeDef = TypedDict(
    "_RequiredColumnSortTypeDef",
    {
        "SortBy": ColumnIdentifierTypeDef,
        "Direction": SortDirectionType,
    },
)
_OptionalColumnSortTypeDef = TypedDict(
    "_OptionalColumnSortTypeDef",
    {
        "AggregationFunction": AggregationFunctionTypeDef,
    },
    total=False,
)


class ColumnSortTypeDef(_RequiredColumnSortTypeDef, _OptionalColumnSortTypeDef):
    pass


_RequiredColumnTooltipItemTypeDef = TypedDict(
    "_RequiredColumnTooltipItemTypeDef",
    {
        "Column": ColumnIdentifierTypeDef,
    },
)
_OptionalColumnTooltipItemTypeDef = TypedDict(
    "_OptionalColumnTooltipItemTypeDef",
    {
        "Label": str,
        "Visibility": VisibilityType,
        "Aggregation": AggregationFunctionTypeDef,
    },
    total=False,
)


class ColumnTooltipItemTypeDef(
    _RequiredColumnTooltipItemTypeDef, _OptionalColumnTooltipItemTypeDef
):
    pass


_RequiredNumericEqualityFilterTypeDef = TypedDict(
    "_RequiredNumericEqualityFilterTypeDef",
    {
        "FilterId": str,
        "Column": ColumnIdentifierTypeDef,
        "MatchOperator": NumericEqualityMatchOperatorType,
        "NullOption": FilterNullOptionType,
    },
)
_OptionalNumericEqualityFilterTypeDef = TypedDict(
    "_OptionalNumericEqualityFilterTypeDef",
    {
        "Value": float,
        "SelectAllOptions": Literal["FILTER_ALL_VALUES"],
        "AggregationFunction": AggregationFunctionTypeDef,
        "ParameterName": str,
    },
    total=False,
)


class NumericEqualityFilterTypeDef(
    _RequiredNumericEqualityFilterTypeDef, _OptionalNumericEqualityFilterTypeDef
):
    pass


_RequiredNumericRangeFilterTypeDef = TypedDict(
    "_RequiredNumericRangeFilterTypeDef",
    {
        "FilterId": str,
        "Column": ColumnIdentifierTypeDef,
        "NullOption": FilterNullOptionType,
    },
)
_OptionalNumericRangeFilterTypeDef = TypedDict(
    "_OptionalNumericRangeFilterTypeDef",
    {
        "IncludeMinimum": bool,
        "IncludeMaximum": bool,
        "RangeMinimum": NumericRangeFilterValueTypeDef,
        "RangeMaximum": NumericRangeFilterValueTypeDef,
        "SelectAllOptions": Literal["FILTER_ALL_VALUES"],
        "AggregationFunction": AggregationFunctionTypeDef,
    },
    total=False,
)


class NumericRangeFilterTypeDef(
    _RequiredNumericRangeFilterTypeDef, _OptionalNumericRangeFilterTypeDef
):
    pass


ReferenceLineDynamicDataConfigurationTypeDef = TypedDict(
    "ReferenceLineDynamicDataConfigurationTypeDef",
    {
        "Column": ColumnIdentifierTypeDef,
        "MeasureAggregationFunction": AggregationFunctionTypeDef,
        "Calculation": NumericalAggregationFunctionTypeDef,
    },
)

CreateRefreshScheduleRequestRequestTypeDef = TypedDict(
    "CreateRefreshScheduleRequestRequestTypeDef",
    {
        "DataSetId": str,
        "AwsAccountId": str,
        "Schedule": RefreshScheduleTypeDef,
    },
)

DescribeRefreshScheduleResponseTypeDef = TypedDict(
    "DescribeRefreshScheduleResponseTypeDef",
    {
        "RefreshSchedule": RefreshScheduleTypeDef,
        "Status": int,
        "RequestId": str,
        "Arn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListRefreshSchedulesResponseTypeDef = TypedDict(
    "ListRefreshSchedulesResponseTypeDef",
    {
        "RefreshSchedules": List[RefreshScheduleTypeDef],
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateRefreshScheduleRequestRequestTypeDef = TypedDict(
    "UpdateRefreshScheduleRequestRequestTypeDef",
    {
        "DataSetId": str,
        "AwsAccountId": str,
        "Schedule": RefreshScheduleTypeDef,
    },
)

RegisteredUserEmbeddingExperienceConfigurationTypeDef = TypedDict(
    "RegisteredUserEmbeddingExperienceConfigurationTypeDef",
    {
        "Dashboard": RegisteredUserDashboardEmbeddingConfigurationTypeDef,
        "QuickSightConsole": RegisteredUserQuickSightConsoleEmbeddingConfigurationTypeDef,
        "QSearchBar": RegisteredUserQSearchBarEmbeddingConfigurationTypeDef,
        "DashboardVisual": RegisteredUserDashboardVisualEmbeddingConfigurationTypeDef,
    },
    total=False,
)

DefaultSectionBasedLayoutConfigurationTypeDef = TypedDict(
    "DefaultSectionBasedLayoutConfigurationTypeDef",
    {
        "CanvasSizeOptions": SectionBasedLayoutCanvasSizeOptionsTypeDef,
    },
)

_RequiredFreeFormLayoutConfigurationTypeDef = TypedDict(
    "_RequiredFreeFormLayoutConfigurationTypeDef",
    {
        "Elements": Sequence[FreeFormLayoutElementTypeDef],
    },
)
_OptionalFreeFormLayoutConfigurationTypeDef = TypedDict(
    "_OptionalFreeFormLayoutConfigurationTypeDef",
    {
        "CanvasSizeOptions": FreeFormLayoutCanvasSizeOptionsTypeDef,
    },
    total=False,
)


class FreeFormLayoutConfigurationTypeDef(
    _RequiredFreeFormLayoutConfigurationTypeDef, _OptionalFreeFormLayoutConfigurationTypeDef
):
    pass


FreeFormSectionLayoutConfigurationTypeDef = TypedDict(
    "FreeFormSectionLayoutConfigurationTypeDef",
    {
        "Elements": Sequence[FreeFormLayoutElementTypeDef],
    },
)

ParameterDeclarationTypeDef = TypedDict(
    "ParameterDeclarationTypeDef",
    {
        "StringParameterDeclaration": StringParameterDeclarationTypeDef,
        "DecimalParameterDeclaration": DecimalParameterDeclarationTypeDef,
        "IntegerParameterDeclaration": IntegerParameterDeclarationTypeDef,
        "DateTimeParameterDeclaration": DateTimeParameterDeclarationTypeDef,
    },
    total=False,
)

ColumnHierarchyTypeDef = TypedDict(
    "ColumnHierarchyTypeDef",
    {
        "ExplicitHierarchy": ExplicitHierarchyTypeDef,
        "DateTimeHierarchy": DateTimeHierarchyTypeDef,
        "PredefinedHierarchy": PredefinedHierarchyTypeDef,
    },
    total=False,
)

DescribeDashboardResponseTypeDef = TypedDict(
    "DescribeDashboardResponseTypeDef",
    {
        "Dashboard": DashboardTypeDef,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredLogicalTableTypeDef = TypedDict(
    "_RequiredLogicalTableTypeDef",
    {
        "Alias": str,
        "Source": LogicalTableSourceTypeDef,
    },
)
_OptionalLogicalTableTypeDef = TypedDict(
    "_OptionalLogicalTableTypeDef",
    {
        "DataTransforms": Sequence[TransformOperationTypeDef],
    },
    total=False,
)


class LogicalTableTypeDef(_RequiredLogicalTableTypeDef, _OptionalLogicalTableTypeDef):
    pass


TemplateTypeDef = TypedDict(
    "TemplateTypeDef",
    {
        "Arn": str,
        "Name": str,
        "Version": TemplateVersionTypeDef,
        "TemplateId": str,
        "LastUpdatedTime": datetime,
        "CreatedTime": datetime,
    },
    total=False,
)

CustomActionSetParametersOperationTypeDef = TypedDict(
    "CustomActionSetParametersOperationTypeDef",
    {
        "ParameterValueConfigurations": Sequence[SetParameterValueConfigurationTypeDef],
    },
)

AxisDisplayOptionsTypeDef = TypedDict(
    "AxisDisplayOptionsTypeDef",
    {
        "TickLabelOptions": AxisTickLabelOptionsTypeDef,
        "AxisLineVisibility": VisibilityType,
        "GridLineVisibility": VisibilityType,
        "DataOptions": AxisDataOptionsTypeDef,
        "ScrollbarOptions": ScrollBarOptionsTypeDef,
        "AxisOffset": str,
    },
    total=False,
)

_RequiredFilterDateTimePickerControlTypeDef = TypedDict(
    "_RequiredFilterDateTimePickerControlTypeDef",
    {
        "FilterControlId": str,
        "Title": str,
        "SourceFilterId": str,
    },
)
_OptionalFilterDateTimePickerControlTypeDef = TypedDict(
    "_OptionalFilterDateTimePickerControlTypeDef",
    {
        "DisplayOptions": DateTimePickerControlDisplayOptionsTypeDef,
        "Type": SheetControlDateTimePickerTypeType,
    },
    total=False,
)


class FilterDateTimePickerControlTypeDef(
    _RequiredFilterDateTimePickerControlTypeDef, _OptionalFilterDateTimePickerControlTypeDef
):
    pass


_RequiredParameterDateTimePickerControlTypeDef = TypedDict(
    "_RequiredParameterDateTimePickerControlTypeDef",
    {
        "ParameterControlId": str,
        "Title": str,
        "SourceParameterName": str,
    },
)
_OptionalParameterDateTimePickerControlTypeDef = TypedDict(
    "_OptionalParameterDateTimePickerControlTypeDef",
    {
        "DisplayOptions": DateTimePickerControlDisplayOptionsTypeDef,
    },
    total=False,
)


class ParameterDateTimePickerControlTypeDef(
    _RequiredParameterDateTimePickerControlTypeDef, _OptionalParameterDateTimePickerControlTypeDef
):
    pass


_RequiredFilterDropDownControlTypeDef = TypedDict(
    "_RequiredFilterDropDownControlTypeDef",
    {
        "FilterControlId": str,
        "Title": str,
        "SourceFilterId": str,
    },
)
_OptionalFilterDropDownControlTypeDef = TypedDict(
    "_OptionalFilterDropDownControlTypeDef",
    {
        "DisplayOptions": DropDownControlDisplayOptionsTypeDef,
        "Type": SheetControlListTypeType,
        "SelectableValues": FilterSelectableValuesTypeDef,
        "CascadingControlConfiguration": CascadingControlConfigurationTypeDef,
    },
    total=False,
)


class FilterDropDownControlTypeDef(
    _RequiredFilterDropDownControlTypeDef, _OptionalFilterDropDownControlTypeDef
):
    pass


_RequiredParameterDropDownControlTypeDef = TypedDict(
    "_RequiredParameterDropDownControlTypeDef",
    {
        "ParameterControlId": str,
        "Title": str,
        "SourceParameterName": str,
    },
)
_OptionalParameterDropDownControlTypeDef = TypedDict(
    "_OptionalParameterDropDownControlTypeDef",
    {
        "DisplayOptions": DropDownControlDisplayOptionsTypeDef,
        "Type": SheetControlListTypeType,
        "SelectableValues": ParameterSelectableValuesTypeDef,
        "CascadingControlConfiguration": CascadingControlConfigurationTypeDef,
    },
    total=False,
)


class ParameterDropDownControlTypeDef(
    _RequiredParameterDropDownControlTypeDef, _OptionalParameterDropDownControlTypeDef
):
    pass


_RequiredFilterListControlTypeDef = TypedDict(
    "_RequiredFilterListControlTypeDef",
    {
        "FilterControlId": str,
        "Title": str,
        "SourceFilterId": str,
    },
)
_OptionalFilterListControlTypeDef = TypedDict(
    "_OptionalFilterListControlTypeDef",
    {
        "DisplayOptions": ListControlDisplayOptionsTypeDef,
        "Type": SheetControlListTypeType,
        "SelectableValues": FilterSelectableValuesTypeDef,
        "CascadingControlConfiguration": CascadingControlConfigurationTypeDef,
    },
    total=False,
)


class FilterListControlTypeDef(
    _RequiredFilterListControlTypeDef, _OptionalFilterListControlTypeDef
):
    pass


_RequiredParameterListControlTypeDef = TypedDict(
    "_RequiredParameterListControlTypeDef",
    {
        "ParameterControlId": str,
        "Title": str,
        "SourceParameterName": str,
    },
)
_OptionalParameterListControlTypeDef = TypedDict(
    "_OptionalParameterListControlTypeDef",
    {
        "DisplayOptions": ListControlDisplayOptionsTypeDef,
        "Type": SheetControlListTypeType,
        "SelectableValues": ParameterSelectableValuesTypeDef,
        "CascadingControlConfiguration": CascadingControlConfigurationTypeDef,
    },
    total=False,
)


class ParameterListControlTypeDef(
    _RequiredParameterListControlTypeDef, _OptionalParameterListControlTypeDef
):
    pass


_RequiredFilterRelativeDateTimeControlTypeDef = TypedDict(
    "_RequiredFilterRelativeDateTimeControlTypeDef",
    {
        "FilterControlId": str,
        "Title": str,
        "SourceFilterId": str,
    },
)
_OptionalFilterRelativeDateTimeControlTypeDef = TypedDict(
    "_OptionalFilterRelativeDateTimeControlTypeDef",
    {
        "DisplayOptions": RelativeDateTimeControlDisplayOptionsTypeDef,
    },
    total=False,
)


class FilterRelativeDateTimeControlTypeDef(
    _RequiredFilterRelativeDateTimeControlTypeDef, _OptionalFilterRelativeDateTimeControlTypeDef
):
    pass


_RequiredFilterSliderControlTypeDef = TypedDict(
    "_RequiredFilterSliderControlTypeDef",
    {
        "FilterControlId": str,
        "Title": str,
        "SourceFilterId": str,
        "MaximumValue": float,
        "MinimumValue": float,
        "StepSize": float,
    },
)
_OptionalFilterSliderControlTypeDef = TypedDict(
    "_OptionalFilterSliderControlTypeDef",
    {
        "DisplayOptions": SliderControlDisplayOptionsTypeDef,
        "Type": SheetControlSliderTypeType,
    },
    total=False,
)


class FilterSliderControlTypeDef(
    _RequiredFilterSliderControlTypeDef, _OptionalFilterSliderControlTypeDef
):
    pass


_RequiredParameterSliderControlTypeDef = TypedDict(
    "_RequiredParameterSliderControlTypeDef",
    {
        "ParameterControlId": str,
        "Title": str,
        "SourceParameterName": str,
        "MaximumValue": float,
        "MinimumValue": float,
        "StepSize": float,
    },
)
_OptionalParameterSliderControlTypeDef = TypedDict(
    "_OptionalParameterSliderControlTypeDef",
    {
        "DisplayOptions": SliderControlDisplayOptionsTypeDef,
    },
    total=False,
)


class ParameterSliderControlTypeDef(
    _RequiredParameterSliderControlTypeDef, _OptionalParameterSliderControlTypeDef
):
    pass


_RequiredFilterTextAreaControlTypeDef = TypedDict(
    "_RequiredFilterTextAreaControlTypeDef",
    {
        "FilterControlId": str,
        "Title": str,
        "SourceFilterId": str,
    },
)
_OptionalFilterTextAreaControlTypeDef = TypedDict(
    "_OptionalFilterTextAreaControlTypeDef",
    {
        "Delimiter": str,
        "DisplayOptions": TextAreaControlDisplayOptionsTypeDef,
    },
    total=False,
)


class FilterTextAreaControlTypeDef(
    _RequiredFilterTextAreaControlTypeDef, _OptionalFilterTextAreaControlTypeDef
):
    pass


_RequiredParameterTextAreaControlTypeDef = TypedDict(
    "_RequiredParameterTextAreaControlTypeDef",
    {
        "ParameterControlId": str,
        "Title": str,
        "SourceParameterName": str,
    },
)
_OptionalParameterTextAreaControlTypeDef = TypedDict(
    "_OptionalParameterTextAreaControlTypeDef",
    {
        "Delimiter": str,
        "DisplayOptions": TextAreaControlDisplayOptionsTypeDef,
    },
    total=False,
)


class ParameterTextAreaControlTypeDef(
    _RequiredParameterTextAreaControlTypeDef, _OptionalParameterTextAreaControlTypeDef
):
    pass


_RequiredFilterTextFieldControlTypeDef = TypedDict(
    "_RequiredFilterTextFieldControlTypeDef",
    {
        "FilterControlId": str,
        "Title": str,
        "SourceFilterId": str,
    },
)
_OptionalFilterTextFieldControlTypeDef = TypedDict(
    "_OptionalFilterTextFieldControlTypeDef",
    {
        "DisplayOptions": TextFieldControlDisplayOptionsTypeDef,
    },
    total=False,
)


class FilterTextFieldControlTypeDef(
    _RequiredFilterTextFieldControlTypeDef, _OptionalFilterTextFieldControlTypeDef
):
    pass


_RequiredParameterTextFieldControlTypeDef = TypedDict(
    "_RequiredParameterTextFieldControlTypeDef",
    {
        "ParameterControlId": str,
        "Title": str,
        "SourceParameterName": str,
    },
)
_OptionalParameterTextFieldControlTypeDef = TypedDict(
    "_OptionalParameterTextFieldControlTypeDef",
    {
        "DisplayOptions": TextFieldControlDisplayOptionsTypeDef,
    },
    total=False,
)


class ParameterTextFieldControlTypeDef(
    _RequiredParameterTextFieldControlTypeDef, _OptionalParameterTextFieldControlTypeDef
):
    pass


SmallMultiplesOptionsTypeDef = TypedDict(
    "SmallMultiplesOptionsTypeDef",
    {
        "MaxVisibleRows": int,
        "MaxVisibleColumns": int,
        "PanelConfiguration": PanelConfigurationTypeDef,
    },
    total=False,
)

TableFieldLinkConfigurationTypeDef = TypedDict(
    "TableFieldLinkConfigurationTypeDef",
    {
        "Target": URLTargetConfigurationType,
        "Content": TableFieldLinkContentConfigurationTypeDef,
    },
)

PivotTableOptionsTypeDef = TypedDict(
    "PivotTableOptionsTypeDef",
    {
        "MetricPlacement": PivotTableMetricPlacementType,
        "SingleMetricVisibility": VisibilityType,
        "ColumnNamesVisibility": VisibilityType,
        "ToggleButtonsVisibility": VisibilityType,
        "ColumnHeaderStyle": TableCellStyleTypeDef,
        "RowHeaderStyle": TableCellStyleTypeDef,
        "CellStyle": TableCellStyleTypeDef,
        "RowFieldNamesStyle": TableCellStyleTypeDef,
        "RowAlternateColorOptions": RowAlternateColorOptionsTypeDef,
        "CollapsedRowDimensionsVisibility": VisibilityType,
    },
    total=False,
)

PivotTotalOptionsTypeDef = TypedDict(
    "PivotTotalOptionsTypeDef",
    {
        "TotalsVisibility": VisibilityType,
        "Placement": TableTotalsPlacementType,
        "ScrollStatus": TableTotalsScrollStatusType,
        "CustomLabel": str,
        "TotalCellStyle": TableCellStyleTypeDef,
        "ValueCellStyle": TableCellStyleTypeDef,
        "MetricHeaderCellStyle": TableCellStyleTypeDef,
    },
    total=False,
)

SubtotalOptionsTypeDef = TypedDict(
    "SubtotalOptionsTypeDef",
    {
        "TotalsVisibility": VisibilityType,
        "CustomLabel": str,
        "FieldLevel": PivotTableSubtotalLevelType,
        "FieldLevelOptions": Sequence[PivotTableFieldSubtotalOptionsTypeDef],
        "TotalCellStyle": TableCellStyleTypeDef,
        "ValueCellStyle": TableCellStyleTypeDef,
        "MetricHeaderCellStyle": TableCellStyleTypeDef,
    },
    total=False,
)

TableOptionsTypeDef = TypedDict(
    "TableOptionsTypeDef",
    {
        "Orientation": TableOrientationType,
        "HeaderStyle": TableCellStyleTypeDef,
        "CellStyle": TableCellStyleTypeDef,
        "RowAlternateColorOptions": RowAlternateColorOptionsTypeDef,
    },
    total=False,
)

TotalOptionsTypeDef = TypedDict(
    "TotalOptionsTypeDef",
    {
        "TotalsVisibility": VisibilityType,
        "Placement": TableTotalsPlacementType,
        "ScrollStatus": TableTotalsScrollStatusType,
        "CustomLabel": str,
        "TotalCellStyle": TableCellStyleTypeDef,
    },
    total=False,
)

GaugeChartArcConditionalFormattingTypeDef = TypedDict(
    "GaugeChartArcConditionalFormattingTypeDef",
    {
        "ForegroundColor": ConditionalFormattingColorTypeDef,
    },
    total=False,
)

GaugeChartPrimaryValueConditionalFormattingTypeDef = TypedDict(
    "GaugeChartPrimaryValueConditionalFormattingTypeDef",
    {
        "TextColor": ConditionalFormattingColorTypeDef,
        "Icon": ConditionalFormattingIconTypeDef,
    },
    total=False,
)

KPIPrimaryValueConditionalFormattingTypeDef = TypedDict(
    "KPIPrimaryValueConditionalFormattingTypeDef",
    {
        "TextColor": ConditionalFormattingColorTypeDef,
        "Icon": ConditionalFormattingIconTypeDef,
    },
    total=False,
)

KPIProgressBarConditionalFormattingTypeDef = TypedDict(
    "KPIProgressBarConditionalFormattingTypeDef",
    {
        "ForegroundColor": ConditionalFormattingColorTypeDef,
    },
    total=False,
)

ShapeConditionalFormatTypeDef = TypedDict(
    "ShapeConditionalFormatTypeDef",
    {
        "BackgroundColor": ConditionalFormattingColorTypeDef,
    },
)

TableRowConditionalFormattingTypeDef = TypedDict(
    "TableRowConditionalFormattingTypeDef",
    {
        "BackgroundColor": ConditionalFormattingColorTypeDef,
        "TextColor": ConditionalFormattingColorTypeDef,
    },
    total=False,
)

TextConditionalFormatTypeDef = TypedDict(
    "TextConditionalFormatTypeDef",
    {
        "BackgroundColor": ConditionalFormattingColorTypeDef,
        "TextColor": ConditionalFormattingColorTypeDef,
        "Icon": ConditionalFormattingIconTypeDef,
    },
    total=False,
)

SheetControlLayoutTypeDef = TypedDict(
    "SheetControlLayoutTypeDef",
    {
        "Configuration": SheetControlLayoutConfigurationTypeDef,
    },
)

DescribeDataSetRefreshPropertiesResponseTypeDef = TypedDict(
    "DescribeDataSetRefreshPropertiesResponseTypeDef",
    {
        "RequestId": str,
        "Status": int,
        "DataSetRefreshProperties": DataSetRefreshPropertiesTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutDataSetRefreshPropertiesRequestRequestTypeDef = TypedDict(
    "PutDataSetRefreshPropertiesRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DataSetId": str,
        "DataSetRefreshProperties": DataSetRefreshPropertiesTypeDef,
    },
)

DataSourceCredentialsTypeDef = TypedDict(
    "DataSourceCredentialsTypeDef",
    {
        "CredentialPair": CredentialPairTypeDef,
        "CopySourceArn": str,
        "SecretArn": str,
    },
    total=False,
)

DescribeDataSourceResponseTypeDef = TypedDict(
    "DescribeDataSourceResponseTypeDef",
    {
        "DataSource": DataSourceTypeDef,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListDataSourcesResponseTypeDef = TypedDict(
    "ListDataSourcesResponseTypeDef",
    {
        "DataSources": List[DataSourceTypeDef],
        "NextToken": str,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateThemeRequestRequestTypeDef = TypedDict(
    "_RequiredCreateThemeRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "ThemeId": str,
        "Name": str,
        "BaseThemeId": str,
        "Configuration": ThemeConfigurationTypeDef,
    },
)
_OptionalCreateThemeRequestRequestTypeDef = TypedDict(
    "_OptionalCreateThemeRequestRequestTypeDef",
    {
        "VersionDescription": str,
        "Permissions": Sequence[ResourcePermissionTypeDef],
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateThemeRequestRequestTypeDef(
    _RequiredCreateThemeRequestRequestTypeDef, _OptionalCreateThemeRequestRequestTypeDef
):
    pass


ThemeVersionTypeDef = TypedDict(
    "ThemeVersionTypeDef",
    {
        "VersionNumber": int,
        "Arn": str,
        "Description": str,
        "BaseThemeId": str,
        "CreatedTime": datetime,
        "Configuration": ThemeConfigurationTypeDef,
        "Errors": List[ThemeErrorTypeDef],
        "Status": ResourceStatusType,
    },
    total=False,
)

_RequiredUpdateThemeRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateThemeRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "ThemeId": str,
        "BaseThemeId": str,
    },
)
_OptionalUpdateThemeRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateThemeRequestRequestTypeDef",
    {
        "Name": str,
        "VersionDescription": str,
        "Configuration": ThemeConfigurationTypeDef,
    },
    total=False,
)


class UpdateThemeRequestRequestTypeDef(
    _RequiredUpdateThemeRequestRequestTypeDef, _OptionalUpdateThemeRequestRequestTypeDef
):
    pass


ComparisonConfigurationTypeDef = TypedDict(
    "ComparisonConfigurationTypeDef",
    {
        "ComparisonMethod": ComparisonMethodType,
        "ComparisonFormat": ComparisonFormatConfigurationTypeDef,
    },
    total=False,
)

DateTimeFormatConfigurationTypeDef = TypedDict(
    "DateTimeFormatConfigurationTypeDef",
    {
        "DateTimeFormat": str,
        "NullValueFormatConfiguration": NullValueFormatConfigurationTypeDef,
        "NumericFormatConfiguration": NumericFormatConfigurationTypeDef,
    },
    total=False,
)

NumberFormatConfigurationTypeDef = TypedDict(
    "NumberFormatConfigurationTypeDef",
    {
        "FormatConfiguration": NumericFormatConfigurationTypeDef,
    },
    total=False,
)

ReferenceLineValueLabelConfigurationTypeDef = TypedDict(
    "ReferenceLineValueLabelConfigurationTypeDef",
    {
        "RelativePosition": ReferenceLineValueLabelRelativePositionType,
        "FormatConfiguration": NumericFormatConfigurationTypeDef,
    },
    total=False,
)

StringFormatConfigurationTypeDef = TypedDict(
    "StringFormatConfigurationTypeDef",
    {
        "NullValueFormatConfiguration": NullValueFormatConfigurationTypeDef,
        "NumericFormatConfiguration": NumericFormatConfigurationTypeDef,
    },
    total=False,
)

_RequiredTopBottomFilterTypeDef = TypedDict(
    "_RequiredTopBottomFilterTypeDef",
    {
        "FilterId": str,
        "Column": ColumnIdentifierTypeDef,
        "AggregationSortConfigurations": Sequence[AggregationSortConfigurationTypeDef],
    },
)
_OptionalTopBottomFilterTypeDef = TypedDict(
    "_OptionalTopBottomFilterTypeDef",
    {
        "Limit": int,
        "TimeGranularity": TimeGranularityType,
        "ParameterName": str,
    },
    total=False,
)


class TopBottomFilterTypeDef(_RequiredTopBottomFilterTypeDef, _OptionalTopBottomFilterTypeDef):
    pass


FieldSortOptionsTypeDef = TypedDict(
    "FieldSortOptionsTypeDef",
    {
        "FieldSort": FieldSortTypeDef,
        "ColumnSort": ColumnSortTypeDef,
    },
    total=False,
)

PivotTableSortByTypeDef = TypedDict(
    "PivotTableSortByTypeDef",
    {
        "Field": FieldSortTypeDef,
        "Column": ColumnSortTypeDef,
        "DataPath": DataPathSortTypeDef,
    },
    total=False,
)

TooltipItemTypeDef = TypedDict(
    "TooltipItemTypeDef",
    {
        "FieldTooltipItem": FieldTooltipItemTypeDef,
        "ColumnTooltipItem": ColumnTooltipItemTypeDef,
    },
    total=False,
)

ReferenceLineDataConfigurationTypeDef = TypedDict(
    "ReferenceLineDataConfigurationTypeDef",
    {
        "StaticConfiguration": ReferenceLineStaticDataConfigurationTypeDef,
        "DynamicConfiguration": ReferenceLineDynamicDataConfigurationTypeDef,
        "AxisBinding": AxisBindingType,
    },
    total=False,
)

_RequiredGenerateEmbedUrlForRegisteredUserRequestRequestTypeDef = TypedDict(
    "_RequiredGenerateEmbedUrlForRegisteredUserRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "UserArn": str,
        "ExperienceConfiguration": RegisteredUserEmbeddingExperienceConfigurationTypeDef,
    },
)
_OptionalGenerateEmbedUrlForRegisteredUserRequestRequestTypeDef = TypedDict(
    "_OptionalGenerateEmbedUrlForRegisteredUserRequestRequestTypeDef",
    {
        "SessionLifetimeInMinutes": int,
        "AllowedDomains": Sequence[str],
    },
    total=False,
)


class GenerateEmbedUrlForRegisteredUserRequestRequestTypeDef(
    _RequiredGenerateEmbedUrlForRegisteredUserRequestRequestTypeDef,
    _OptionalGenerateEmbedUrlForRegisteredUserRequestRequestTypeDef,
):
    pass


DefaultPaginatedLayoutConfigurationTypeDef = TypedDict(
    "DefaultPaginatedLayoutConfigurationTypeDef",
    {
        "SectionBased": DefaultSectionBasedLayoutConfigurationTypeDef,
    },
    total=False,
)

SectionLayoutConfigurationTypeDef = TypedDict(
    "SectionLayoutConfigurationTypeDef",
    {
        "FreeFormLayout": FreeFormSectionLayoutConfigurationTypeDef,
    },
)

_RequiredCreateDataSetRequestRequestTypeDef = TypedDict(
    "_RequiredCreateDataSetRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DataSetId": str,
        "Name": str,
        "PhysicalTableMap": Mapping[str, PhysicalTableTypeDef],
        "ImportMode": DataSetImportModeType,
    },
)
_OptionalCreateDataSetRequestRequestTypeDef = TypedDict(
    "_OptionalCreateDataSetRequestRequestTypeDef",
    {
        "LogicalTableMap": Mapping[str, LogicalTableTypeDef],
        "ColumnGroups": Sequence[ColumnGroupTypeDef],
        "FieldFolders": Mapping[str, FieldFolderTypeDef],
        "Permissions": Sequence[ResourcePermissionTypeDef],
        "RowLevelPermissionDataSet": RowLevelPermissionDataSetTypeDef,
        "RowLevelPermissionTagConfiguration": RowLevelPermissionTagConfigurationTypeDef,
        "ColumnLevelPermissionRules": Sequence[ColumnLevelPermissionRuleTypeDef],
        "Tags": Sequence[TagTypeDef],
        "DataSetUsageConfiguration": DataSetUsageConfigurationTypeDef,
    },
    total=False,
)


class CreateDataSetRequestRequestTypeDef(
    _RequiredCreateDataSetRequestRequestTypeDef, _OptionalCreateDataSetRequestRequestTypeDef
):
    pass


DataSetTypeDef = TypedDict(
    "DataSetTypeDef",
    {
        "Arn": str,
        "DataSetId": str,
        "Name": str,
        "CreatedTime": datetime,
        "LastUpdatedTime": datetime,
        "PhysicalTableMap": Dict[str, PhysicalTableTypeDef],
        "LogicalTableMap": Dict[str, LogicalTableTypeDef],
        "OutputColumns": List[OutputColumnTypeDef],
        "ImportMode": DataSetImportModeType,
        "ConsumedSpiceCapacityInBytes": int,
        "ColumnGroups": List[ColumnGroupTypeDef],
        "FieldFolders": Dict[str, FieldFolderTypeDef],
        "RowLevelPermissionDataSet": RowLevelPermissionDataSetTypeDef,
        "RowLevelPermissionTagConfiguration": RowLevelPermissionTagConfigurationTypeDef,
        "ColumnLevelPermissionRules": List[ColumnLevelPermissionRuleTypeDef],
        "DataSetUsageConfiguration": DataSetUsageConfigurationTypeDef,
    },
    total=False,
)

_RequiredUpdateDataSetRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateDataSetRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DataSetId": str,
        "Name": str,
        "PhysicalTableMap": Mapping[str, PhysicalTableTypeDef],
        "ImportMode": DataSetImportModeType,
    },
)
_OptionalUpdateDataSetRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateDataSetRequestRequestTypeDef",
    {
        "LogicalTableMap": Mapping[str, LogicalTableTypeDef],
        "ColumnGroups": Sequence[ColumnGroupTypeDef],
        "FieldFolders": Mapping[str, FieldFolderTypeDef],
        "RowLevelPermissionDataSet": RowLevelPermissionDataSetTypeDef,
        "RowLevelPermissionTagConfiguration": RowLevelPermissionTagConfigurationTypeDef,
        "ColumnLevelPermissionRules": Sequence[ColumnLevelPermissionRuleTypeDef],
        "DataSetUsageConfiguration": DataSetUsageConfigurationTypeDef,
    },
    total=False,
)


class UpdateDataSetRequestRequestTypeDef(
    _RequiredUpdateDataSetRequestRequestTypeDef, _OptionalUpdateDataSetRequestRequestTypeDef
):
    pass


DescribeTemplateResponseTypeDef = TypedDict(
    "DescribeTemplateResponseTypeDef",
    {
        "Template": TemplateTypeDef,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

VisualCustomActionOperationTypeDef = TypedDict(
    "VisualCustomActionOperationTypeDef",
    {
        "FilterOperation": CustomActionFilterOperationTypeDef,
        "NavigationOperation": CustomActionNavigationOperationTypeDef,
        "URLOperation": CustomActionURLOperationTypeDef,
        "SetParametersOperation": CustomActionSetParametersOperationTypeDef,
    },
    total=False,
)

LineSeriesAxisDisplayOptionsTypeDef = TypedDict(
    "LineSeriesAxisDisplayOptionsTypeDef",
    {
        "AxisOptions": AxisDisplayOptionsTypeDef,
        "MissingDataConfigurations": Sequence[MissingDataConfigurationTypeDef],
    },
    total=False,
)

FilterControlTypeDef = TypedDict(
    "FilterControlTypeDef",
    {
        "DateTimePicker": FilterDateTimePickerControlTypeDef,
        "List": FilterListControlTypeDef,
        "Dropdown": FilterDropDownControlTypeDef,
        "TextField": FilterTextFieldControlTypeDef,
        "TextArea": FilterTextAreaControlTypeDef,
        "Slider": FilterSliderControlTypeDef,
        "RelativeDateTime": FilterRelativeDateTimeControlTypeDef,
    },
    total=False,
)

ParameterControlTypeDef = TypedDict(
    "ParameterControlTypeDef",
    {
        "DateTimePicker": ParameterDateTimePickerControlTypeDef,
        "List": ParameterListControlTypeDef,
        "Dropdown": ParameterDropDownControlTypeDef,
        "TextField": ParameterTextFieldControlTypeDef,
        "TextArea": ParameterTextAreaControlTypeDef,
        "Slider": ParameterSliderControlTypeDef,
    },
    total=False,
)

TableFieldURLConfigurationTypeDef = TypedDict(
    "TableFieldURLConfigurationTypeDef",
    {
        "LinkConfiguration": TableFieldLinkConfigurationTypeDef,
        "ImageConfiguration": TableFieldImageConfigurationTypeDef,
    },
    total=False,
)

PivotTableTotalOptionsTypeDef = TypedDict(
    "PivotTableTotalOptionsTypeDef",
    {
        "RowSubtotalOptions": SubtotalOptionsTypeDef,
        "ColumnSubtotalOptions": SubtotalOptionsTypeDef,
        "RowTotalOptions": PivotTotalOptionsTypeDef,
        "ColumnTotalOptions": PivotTotalOptionsTypeDef,
    },
    total=False,
)

GaugeChartConditionalFormattingOptionTypeDef = TypedDict(
    "GaugeChartConditionalFormattingOptionTypeDef",
    {
        "PrimaryValue": GaugeChartPrimaryValueConditionalFormattingTypeDef,
        "Arc": GaugeChartArcConditionalFormattingTypeDef,
    },
    total=False,
)

KPIConditionalFormattingOptionTypeDef = TypedDict(
    "KPIConditionalFormattingOptionTypeDef",
    {
        "PrimaryValue": KPIPrimaryValueConditionalFormattingTypeDef,
        "ProgressBar": KPIProgressBarConditionalFormattingTypeDef,
    },
    total=False,
)

_RequiredFilledMapShapeConditionalFormattingTypeDef = TypedDict(
    "_RequiredFilledMapShapeConditionalFormattingTypeDef",
    {
        "FieldId": str,
    },
)
_OptionalFilledMapShapeConditionalFormattingTypeDef = TypedDict(
    "_OptionalFilledMapShapeConditionalFormattingTypeDef",
    {
        "Format": ShapeConditionalFormatTypeDef,
    },
    total=False,
)


class FilledMapShapeConditionalFormattingTypeDef(
    _RequiredFilledMapShapeConditionalFormattingTypeDef,
    _OptionalFilledMapShapeConditionalFormattingTypeDef,
):
    pass


_RequiredPivotTableCellConditionalFormattingTypeDef = TypedDict(
    "_RequiredPivotTableCellConditionalFormattingTypeDef",
    {
        "FieldId": str,
    },
)
_OptionalPivotTableCellConditionalFormattingTypeDef = TypedDict(
    "_OptionalPivotTableCellConditionalFormattingTypeDef",
    {
        "TextFormat": TextConditionalFormatTypeDef,
        "Scope": PivotTableConditionalFormattingScopeTypeDef,
    },
    total=False,
)


class PivotTableCellConditionalFormattingTypeDef(
    _RequiredPivotTableCellConditionalFormattingTypeDef,
    _OptionalPivotTableCellConditionalFormattingTypeDef,
):
    pass


_RequiredTableCellConditionalFormattingTypeDef = TypedDict(
    "_RequiredTableCellConditionalFormattingTypeDef",
    {
        "FieldId": str,
    },
)
_OptionalTableCellConditionalFormattingTypeDef = TypedDict(
    "_OptionalTableCellConditionalFormattingTypeDef",
    {
        "TextFormat": TextConditionalFormatTypeDef,
    },
    total=False,
)


class TableCellConditionalFormattingTypeDef(
    _RequiredTableCellConditionalFormattingTypeDef, _OptionalTableCellConditionalFormattingTypeDef
):
    pass


_RequiredCreateDataSourceRequestRequestTypeDef = TypedDict(
    "_RequiredCreateDataSourceRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DataSourceId": str,
        "Name": str,
        "Type": DataSourceTypeType,
    },
)
_OptionalCreateDataSourceRequestRequestTypeDef = TypedDict(
    "_OptionalCreateDataSourceRequestRequestTypeDef",
    {
        "DataSourceParameters": DataSourceParametersTypeDef,
        "Credentials": DataSourceCredentialsTypeDef,
        "Permissions": Sequence[ResourcePermissionTypeDef],
        "VpcConnectionProperties": VpcConnectionPropertiesTypeDef,
        "SslProperties": SslPropertiesTypeDef,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateDataSourceRequestRequestTypeDef(
    _RequiredCreateDataSourceRequestRequestTypeDef, _OptionalCreateDataSourceRequestRequestTypeDef
):
    pass


_RequiredUpdateDataSourceRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateDataSourceRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DataSourceId": str,
        "Name": str,
    },
)
_OptionalUpdateDataSourceRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateDataSourceRequestRequestTypeDef",
    {
        "DataSourceParameters": DataSourceParametersTypeDef,
        "Credentials": DataSourceCredentialsTypeDef,
        "VpcConnectionProperties": VpcConnectionPropertiesTypeDef,
        "SslProperties": SslPropertiesTypeDef,
    },
    total=False,
)


class UpdateDataSourceRequestRequestTypeDef(
    _RequiredUpdateDataSourceRequestRequestTypeDef, _OptionalUpdateDataSourceRequestRequestTypeDef
):
    pass


ThemeTypeDef = TypedDict(
    "ThemeTypeDef",
    {
        "Arn": str,
        "Name": str,
        "ThemeId": str,
        "Version": ThemeVersionTypeDef,
        "CreatedTime": datetime,
        "LastUpdatedTime": datetime,
        "Type": ThemeTypeType,
    },
    total=False,
)

GaugeChartOptionsTypeDef = TypedDict(
    "GaugeChartOptionsTypeDef",
    {
        "PrimaryValueDisplayType": PrimaryValueDisplayTypeType,
        "Comparison": ComparisonConfigurationTypeDef,
        "ArcAxis": ArcAxisConfigurationTypeDef,
        "Arc": ArcConfigurationTypeDef,
        "PrimaryValueFontConfiguration": FontConfigurationTypeDef,
    },
    total=False,
)

KPIOptionsTypeDef = TypedDict(
    "KPIOptionsTypeDef",
    {
        "ProgressBar": ProgressBarOptionsTypeDef,
        "TrendArrows": TrendArrowOptionsTypeDef,
        "SecondaryValue": SecondaryValueOptionsTypeDef,
        "Comparison": ComparisonConfigurationTypeDef,
        "PrimaryValueDisplayType": PrimaryValueDisplayTypeType,
        "PrimaryValueFontConfiguration": FontConfigurationTypeDef,
        "SecondaryValueFontConfiguration": FontConfigurationTypeDef,
    },
    total=False,
)

_RequiredDateDimensionFieldTypeDef = TypedDict(
    "_RequiredDateDimensionFieldTypeDef",
    {
        "FieldId": str,
        "Column": ColumnIdentifierTypeDef,
    },
)
_OptionalDateDimensionFieldTypeDef = TypedDict(
    "_OptionalDateDimensionFieldTypeDef",
    {
        "DateGranularity": TimeGranularityType,
        "HierarchyId": str,
        "FormatConfiguration": DateTimeFormatConfigurationTypeDef,
    },
    total=False,
)


class DateDimensionFieldTypeDef(
    _RequiredDateDimensionFieldTypeDef, _OptionalDateDimensionFieldTypeDef
):
    pass


_RequiredDateMeasureFieldTypeDef = TypedDict(
    "_RequiredDateMeasureFieldTypeDef",
    {
        "FieldId": str,
        "Column": ColumnIdentifierTypeDef,
    },
)
_OptionalDateMeasureFieldTypeDef = TypedDict(
    "_OptionalDateMeasureFieldTypeDef",
    {
        "AggregationFunction": DateAggregationFunctionType,
        "FormatConfiguration": DateTimeFormatConfigurationTypeDef,
    },
    total=False,
)


class DateMeasureFieldTypeDef(_RequiredDateMeasureFieldTypeDef, _OptionalDateMeasureFieldTypeDef):
    pass


_RequiredNumericalDimensionFieldTypeDef = TypedDict(
    "_RequiredNumericalDimensionFieldTypeDef",
    {
        "FieldId": str,
        "Column": ColumnIdentifierTypeDef,
    },
)
_OptionalNumericalDimensionFieldTypeDef = TypedDict(
    "_OptionalNumericalDimensionFieldTypeDef",
    {
        "HierarchyId": str,
        "FormatConfiguration": NumberFormatConfigurationTypeDef,
    },
    total=False,
)


class NumericalDimensionFieldTypeDef(
    _RequiredNumericalDimensionFieldTypeDef, _OptionalNumericalDimensionFieldTypeDef
):
    pass


_RequiredNumericalMeasureFieldTypeDef = TypedDict(
    "_RequiredNumericalMeasureFieldTypeDef",
    {
        "FieldId": str,
        "Column": ColumnIdentifierTypeDef,
    },
)
_OptionalNumericalMeasureFieldTypeDef = TypedDict(
    "_OptionalNumericalMeasureFieldTypeDef",
    {
        "AggregationFunction": NumericalAggregationFunctionTypeDef,
        "FormatConfiguration": NumberFormatConfigurationTypeDef,
    },
    total=False,
)


class NumericalMeasureFieldTypeDef(
    _RequiredNumericalMeasureFieldTypeDef, _OptionalNumericalMeasureFieldTypeDef
):
    pass


ReferenceLineLabelConfigurationTypeDef = TypedDict(
    "ReferenceLineLabelConfigurationTypeDef",
    {
        "ValueLabelConfiguration": ReferenceLineValueLabelConfigurationTypeDef,
        "CustomLabelConfiguration": ReferenceLineCustomLabelConfigurationTypeDef,
        "FontConfiguration": FontConfigurationTypeDef,
        "FontColor": str,
        "HorizontalPosition": ReferenceLineLabelHorizontalPositionType,
        "VerticalPosition": ReferenceLineLabelVerticalPositionType,
    },
    total=False,
)

_RequiredCategoricalDimensionFieldTypeDef = TypedDict(
    "_RequiredCategoricalDimensionFieldTypeDef",
    {
        "FieldId": str,
        "Column": ColumnIdentifierTypeDef,
    },
)
_OptionalCategoricalDimensionFieldTypeDef = TypedDict(
    "_OptionalCategoricalDimensionFieldTypeDef",
    {
        "HierarchyId": str,
        "FormatConfiguration": StringFormatConfigurationTypeDef,
    },
    total=False,
)


class CategoricalDimensionFieldTypeDef(
    _RequiredCategoricalDimensionFieldTypeDef, _OptionalCategoricalDimensionFieldTypeDef
):
    pass


_RequiredCategoricalMeasureFieldTypeDef = TypedDict(
    "_RequiredCategoricalMeasureFieldTypeDef",
    {
        "FieldId": str,
        "Column": ColumnIdentifierTypeDef,
    },
)
_OptionalCategoricalMeasureFieldTypeDef = TypedDict(
    "_OptionalCategoricalMeasureFieldTypeDef",
    {
        "AggregationFunction": CategoricalAggregationFunctionType,
        "FormatConfiguration": StringFormatConfigurationTypeDef,
    },
    total=False,
)


class CategoricalMeasureFieldTypeDef(
    _RequiredCategoricalMeasureFieldTypeDef, _OptionalCategoricalMeasureFieldTypeDef
):
    pass


FormatConfigurationTypeDef = TypedDict(
    "FormatConfigurationTypeDef",
    {
        "StringFormatConfiguration": StringFormatConfigurationTypeDef,
        "NumberFormatConfiguration": NumberFormatConfigurationTypeDef,
        "DateTimeFormatConfiguration": DateTimeFormatConfigurationTypeDef,
    },
    total=False,
)

FilterTypeDef = TypedDict(
    "FilterTypeDef",
    {
        "CategoryFilter": CategoryFilterTypeDef,
        "NumericRangeFilter": NumericRangeFilterTypeDef,
        "NumericEqualityFilter": NumericEqualityFilterTypeDef,
        "TimeEqualityFilter": TimeEqualityFilterTypeDef,
        "TimeRangeFilter": TimeRangeFilterTypeDef,
        "RelativeDatesFilter": RelativeDatesFilterTypeDef,
        "TopBottomFilter": TopBottomFilterTypeDef,
    },
    total=False,
)

BarChartSortConfigurationTypeDef = TypedDict(
    "BarChartSortConfigurationTypeDef",
    {
        "CategorySort": Sequence[FieldSortOptionsTypeDef],
        "CategoryItemsLimit": ItemsLimitConfigurationTypeDef,
        "ColorSort": Sequence[FieldSortOptionsTypeDef],
        "ColorItemsLimit": ItemsLimitConfigurationTypeDef,
        "SmallMultiplesSort": Sequence[FieldSortOptionsTypeDef],
        "SmallMultiplesLimitConfiguration": ItemsLimitConfigurationTypeDef,
    },
    total=False,
)

BoxPlotSortConfigurationTypeDef = TypedDict(
    "BoxPlotSortConfigurationTypeDef",
    {
        "CategorySort": Sequence[FieldSortOptionsTypeDef],
        "PaginationConfiguration": PaginationConfigurationTypeDef,
    },
    total=False,
)

ComboChartSortConfigurationTypeDef = TypedDict(
    "ComboChartSortConfigurationTypeDef",
    {
        "CategorySort": Sequence[FieldSortOptionsTypeDef],
        "CategoryItemsLimit": ItemsLimitConfigurationTypeDef,
        "ColorSort": Sequence[FieldSortOptionsTypeDef],
        "ColorItemsLimit": ItemsLimitConfigurationTypeDef,
    },
    total=False,
)

FilledMapSortConfigurationTypeDef = TypedDict(
    "FilledMapSortConfigurationTypeDef",
    {
        "CategorySort": Sequence[FieldSortOptionsTypeDef],
    },
    total=False,
)

FunnelChartSortConfigurationTypeDef = TypedDict(
    "FunnelChartSortConfigurationTypeDef",
    {
        "CategorySort": Sequence[FieldSortOptionsTypeDef],
        "CategoryItemsLimit": ItemsLimitConfigurationTypeDef,
    },
    total=False,
)

HeatMapSortConfigurationTypeDef = TypedDict(
    "HeatMapSortConfigurationTypeDef",
    {
        "HeatMapRowSort": Sequence[FieldSortOptionsTypeDef],
        "HeatMapColumnSort": Sequence[FieldSortOptionsTypeDef],
        "HeatMapRowItemsLimitConfiguration": ItemsLimitConfigurationTypeDef,
        "HeatMapColumnItemsLimitConfiguration": ItemsLimitConfigurationTypeDef,
    },
    total=False,
)

KPISortConfigurationTypeDef = TypedDict(
    "KPISortConfigurationTypeDef",
    {
        "TrendGroupSort": Sequence[FieldSortOptionsTypeDef],
    },
    total=False,
)

LineChartSortConfigurationTypeDef = TypedDict(
    "LineChartSortConfigurationTypeDef",
    {
        "CategorySort": Sequence[FieldSortOptionsTypeDef],
        "CategoryItemsLimitConfiguration": ItemsLimitConfigurationTypeDef,
        "ColorItemsLimitConfiguration": ItemsLimitConfigurationTypeDef,
        "SmallMultiplesSort": Sequence[FieldSortOptionsTypeDef],
        "SmallMultiplesLimitConfiguration": ItemsLimitConfigurationTypeDef,
    },
    total=False,
)

PieChartSortConfigurationTypeDef = TypedDict(
    "PieChartSortConfigurationTypeDef",
    {
        "CategorySort": Sequence[FieldSortOptionsTypeDef],
        "CategoryItemsLimit": ItemsLimitConfigurationTypeDef,
        "SmallMultiplesSort": Sequence[FieldSortOptionsTypeDef],
        "SmallMultiplesLimitConfiguration": ItemsLimitConfigurationTypeDef,
    },
    total=False,
)

RadarChartSortConfigurationTypeDef = TypedDict(
    "RadarChartSortConfigurationTypeDef",
    {
        "CategorySort": Sequence[FieldSortOptionsTypeDef],
        "CategoryItemsLimit": ItemsLimitConfigurationTypeDef,
        "ColorSort": Sequence[FieldSortOptionsTypeDef],
        "ColorItemsLimit": ItemsLimitConfigurationTypeDef,
    },
    total=False,
)

SankeyDiagramSortConfigurationTypeDef = TypedDict(
    "SankeyDiagramSortConfigurationTypeDef",
    {
        "WeightSort": Sequence[FieldSortOptionsTypeDef],
        "SourceItemsLimit": ItemsLimitConfigurationTypeDef,
        "DestinationItemsLimit": ItemsLimitConfigurationTypeDef,
    },
    total=False,
)

TableSortConfigurationTypeDef = TypedDict(
    "TableSortConfigurationTypeDef",
    {
        "RowSort": Sequence[FieldSortOptionsTypeDef],
        "PaginationConfiguration": PaginationConfigurationTypeDef,
    },
    total=False,
)

TreeMapSortConfigurationTypeDef = TypedDict(
    "TreeMapSortConfigurationTypeDef",
    {
        "TreeMapSort": Sequence[FieldSortOptionsTypeDef],
        "TreeMapGroupItemsLimitConfiguration": ItemsLimitConfigurationTypeDef,
    },
    total=False,
)

WaterfallChartSortConfigurationTypeDef = TypedDict(
    "WaterfallChartSortConfigurationTypeDef",
    {
        "CategorySort": Sequence[FieldSortOptionsTypeDef],
        "BreakdownItemsLimit": ItemsLimitConfigurationTypeDef,
    },
    total=False,
)

WordCloudSortConfigurationTypeDef = TypedDict(
    "WordCloudSortConfigurationTypeDef",
    {
        "CategoryItemsLimit": ItemsLimitConfigurationTypeDef,
        "CategorySort": Sequence[FieldSortOptionsTypeDef],
    },
    total=False,
)

PivotFieldSortOptionsTypeDef = TypedDict(
    "PivotFieldSortOptionsTypeDef",
    {
        "FieldId": str,
        "SortBy": PivotTableSortByTypeDef,
    },
)

FieldBasedTooltipTypeDef = TypedDict(
    "FieldBasedTooltipTypeDef",
    {
        "AggregationVisibility": VisibilityType,
        "TooltipTitleType": TooltipTitleTypeType,
        "TooltipFields": Sequence[TooltipItemTypeDef],
    },
    total=False,
)

DefaultNewSheetConfigurationTypeDef = TypedDict(
    "DefaultNewSheetConfigurationTypeDef",
    {
        "InteractiveLayoutConfiguration": DefaultInteractiveLayoutConfigurationTypeDef,
        "PaginatedLayoutConfiguration": DefaultPaginatedLayoutConfigurationTypeDef,
        "SheetContentType": SheetContentTypeType,
    },
    total=False,
)

BodySectionContentTypeDef = TypedDict(
    "BodySectionContentTypeDef",
    {
        "Layout": SectionLayoutConfigurationTypeDef,
    },
    total=False,
)

_RequiredHeaderFooterSectionConfigurationTypeDef = TypedDict(
    "_RequiredHeaderFooterSectionConfigurationTypeDef",
    {
        "SectionId": str,
        "Layout": SectionLayoutConfigurationTypeDef,
    },
)
_OptionalHeaderFooterSectionConfigurationTypeDef = TypedDict(
    "_OptionalHeaderFooterSectionConfigurationTypeDef",
    {
        "Style": SectionStyleTypeDef,
    },
    total=False,
)


class HeaderFooterSectionConfigurationTypeDef(
    _RequiredHeaderFooterSectionConfigurationTypeDef,
    _OptionalHeaderFooterSectionConfigurationTypeDef,
):
    pass


DescribeDataSetResponseTypeDef = TypedDict(
    "DescribeDataSetResponseTypeDef",
    {
        "DataSet": DataSetTypeDef,
        "RequestId": str,
        "Status": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredVisualCustomActionTypeDef = TypedDict(
    "_RequiredVisualCustomActionTypeDef",
    {
        "CustomActionId": str,
        "Name": str,
        "Trigger": VisualCustomActionTriggerType,
        "ActionOperations": Sequence[VisualCustomActionOperationTypeDef],
    },
)
_OptionalVisualCustomActionTypeDef = TypedDict(
    "_OptionalVisualCustomActionTypeDef",
    {
        "Status": WidgetStatusType,
    },
    total=False,
)


class VisualCustomActionTypeDef(
    _RequiredVisualCustomActionTypeDef, _OptionalVisualCustomActionTypeDef
):
    pass


_RequiredTableFieldOptionTypeDef = TypedDict(
    "_RequiredTableFieldOptionTypeDef",
    {
        "FieldId": str,
    },
)
_OptionalTableFieldOptionTypeDef = TypedDict(
    "_OptionalTableFieldOptionTypeDef",
    {
        "Width": str,
        "CustomLabel": str,
        "Visibility": VisibilityType,
        "URLStyling": TableFieldURLConfigurationTypeDef,
    },
    total=False,
)


class TableFieldOptionTypeDef(_RequiredTableFieldOptionTypeDef, _OptionalTableFieldOptionTypeDef):
    pass


GaugeChartConditionalFormattingTypeDef = TypedDict(
    "GaugeChartConditionalFormattingTypeDef",
    {
        "ConditionalFormattingOptions": Sequence[GaugeChartConditionalFormattingOptionTypeDef],
    },
    total=False,
)

KPIConditionalFormattingTypeDef = TypedDict(
    "KPIConditionalFormattingTypeDef",
    {
        "ConditionalFormattingOptions": Sequence[KPIConditionalFormattingOptionTypeDef],
    },
    total=False,
)

FilledMapConditionalFormattingOptionTypeDef = TypedDict(
    "FilledMapConditionalFormattingOptionTypeDef",
    {
        "Shape": FilledMapShapeConditionalFormattingTypeDef,
    },
)

PivotTableConditionalFormattingOptionTypeDef = TypedDict(
    "PivotTableConditionalFormattingOptionTypeDef",
    {
        "Cell": PivotTableCellConditionalFormattingTypeDef,
    },
    total=False,
)

TableConditionalFormattingOptionTypeDef = TypedDict(
    "TableConditionalFormattingOptionTypeDef",
    {
        "Cell": TableCellConditionalFormattingTypeDef,
        "Row": TableRowConditionalFormattingTypeDef,
    },
    total=False,
)

DescribeThemeResponseTypeDef = TypedDict(
    "DescribeThemeResponseTypeDef",
    {
        "Theme": ThemeTypeDef,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredReferenceLineTypeDef = TypedDict(
    "_RequiredReferenceLineTypeDef",
    {
        "DataConfiguration": ReferenceLineDataConfigurationTypeDef,
    },
)
_OptionalReferenceLineTypeDef = TypedDict(
    "_OptionalReferenceLineTypeDef",
    {
        "Status": WidgetStatusType,
        "StyleConfiguration": ReferenceLineStyleConfigurationTypeDef,
        "LabelConfiguration": ReferenceLineLabelConfigurationTypeDef,
    },
    total=False,
)


class ReferenceLineTypeDef(_RequiredReferenceLineTypeDef, _OptionalReferenceLineTypeDef):
    pass


DimensionFieldTypeDef = TypedDict(
    "DimensionFieldTypeDef",
    {
        "NumericalDimensionField": NumericalDimensionFieldTypeDef,
        "CategoricalDimensionField": CategoricalDimensionFieldTypeDef,
        "DateDimensionField": DateDimensionFieldTypeDef,
    },
    total=False,
)

MeasureFieldTypeDef = TypedDict(
    "MeasureFieldTypeDef",
    {
        "NumericalMeasureField": NumericalMeasureFieldTypeDef,
        "CategoricalMeasureField": CategoricalMeasureFieldTypeDef,
        "DateMeasureField": DateMeasureFieldTypeDef,
        "CalculatedMeasureField": CalculatedMeasureFieldTypeDef,
    },
    total=False,
)

_RequiredColumnConfigurationTypeDef = TypedDict(
    "_RequiredColumnConfigurationTypeDef",
    {
        "Column": ColumnIdentifierTypeDef,
    },
)
_OptionalColumnConfigurationTypeDef = TypedDict(
    "_OptionalColumnConfigurationTypeDef",
    {
        "FormatConfiguration": FormatConfigurationTypeDef,
        "Role": ColumnRoleType,
    },
    total=False,
)


class ColumnConfigurationTypeDef(
    _RequiredColumnConfigurationTypeDef, _OptionalColumnConfigurationTypeDef
):
    pass


_RequiredUnaggregatedFieldTypeDef = TypedDict(
    "_RequiredUnaggregatedFieldTypeDef",
    {
        "FieldId": str,
        "Column": ColumnIdentifierTypeDef,
    },
)
_OptionalUnaggregatedFieldTypeDef = TypedDict(
    "_OptionalUnaggregatedFieldTypeDef",
    {
        "FormatConfiguration": FormatConfigurationTypeDef,
    },
    total=False,
)


class UnaggregatedFieldTypeDef(
    _RequiredUnaggregatedFieldTypeDef, _OptionalUnaggregatedFieldTypeDef
):
    pass


_RequiredFilterGroupTypeDef = TypedDict(
    "_RequiredFilterGroupTypeDef",
    {
        "FilterGroupId": str,
        "Filters": Sequence[FilterTypeDef],
        "ScopeConfiguration": FilterScopeConfigurationTypeDef,
        "CrossDataset": CrossDatasetTypesType,
    },
)
_OptionalFilterGroupTypeDef = TypedDict(
    "_OptionalFilterGroupTypeDef",
    {
        "Status": WidgetStatusType,
    },
    total=False,
)


class FilterGroupTypeDef(_RequiredFilterGroupTypeDef, _OptionalFilterGroupTypeDef):
    pass


PivotTableSortConfigurationTypeDef = TypedDict(
    "PivotTableSortConfigurationTypeDef",
    {
        "FieldSortOptions": Sequence[PivotFieldSortOptionsTypeDef],
    },
    total=False,
)

TooltipOptionsTypeDef = TypedDict(
    "TooltipOptionsTypeDef",
    {
        "TooltipVisibility": VisibilityType,
        "SelectedTooltipType": SelectedTooltipTypeType,
        "FieldBasedTooltip": FieldBasedTooltipTypeDef,
    },
    total=False,
)

AnalysisDefaultsTypeDef = TypedDict(
    "AnalysisDefaultsTypeDef",
    {
        "DefaultNewSheetConfiguration": DefaultNewSheetConfigurationTypeDef,
    },
)

_RequiredBodySectionConfigurationTypeDef = TypedDict(
    "_RequiredBodySectionConfigurationTypeDef",
    {
        "SectionId": str,
        "Content": BodySectionContentTypeDef,
    },
)
_OptionalBodySectionConfigurationTypeDef = TypedDict(
    "_OptionalBodySectionConfigurationTypeDef",
    {
        "Style": SectionStyleTypeDef,
        "PageBreakConfiguration": SectionPageBreakConfigurationTypeDef,
    },
    total=False,
)


class BodySectionConfigurationTypeDef(
    _RequiredBodySectionConfigurationTypeDef, _OptionalBodySectionConfigurationTypeDef
):
    pass


_RequiredCustomContentVisualTypeDef = TypedDict(
    "_RequiredCustomContentVisualTypeDef",
    {
        "VisualId": str,
        "DataSetIdentifier": str,
    },
)
_OptionalCustomContentVisualTypeDef = TypedDict(
    "_OptionalCustomContentVisualTypeDef",
    {
        "Title": VisualTitleLabelOptionsTypeDef,
        "Subtitle": VisualSubtitleLabelOptionsTypeDef,
        "ChartConfiguration": CustomContentConfigurationTypeDef,
        "Actions": Sequence[VisualCustomActionTypeDef],
    },
    total=False,
)


class CustomContentVisualTypeDef(
    _RequiredCustomContentVisualTypeDef, _OptionalCustomContentVisualTypeDef
):
    pass


_RequiredEmptyVisualTypeDef = TypedDict(
    "_RequiredEmptyVisualTypeDef",
    {
        "VisualId": str,
        "DataSetIdentifier": str,
    },
)
_OptionalEmptyVisualTypeDef = TypedDict(
    "_OptionalEmptyVisualTypeDef",
    {
        "Actions": Sequence[VisualCustomActionTypeDef],
    },
    total=False,
)


class EmptyVisualTypeDef(_RequiredEmptyVisualTypeDef, _OptionalEmptyVisualTypeDef):
    pass


TableFieldOptionsTypeDef = TypedDict(
    "TableFieldOptionsTypeDef",
    {
        "SelectedFieldOptions": Sequence[TableFieldOptionTypeDef],
        "Order": Sequence[str],
    },
    total=False,
)

FilledMapConditionalFormattingTypeDef = TypedDict(
    "FilledMapConditionalFormattingTypeDef",
    {
        "ConditionalFormattingOptions": Sequence[FilledMapConditionalFormattingOptionTypeDef],
    },
)

PivotTableConditionalFormattingTypeDef = TypedDict(
    "PivotTableConditionalFormattingTypeDef",
    {
        "ConditionalFormattingOptions": Sequence[PivotTableConditionalFormattingOptionTypeDef],
    },
    total=False,
)

TableConditionalFormattingTypeDef = TypedDict(
    "TableConditionalFormattingTypeDef",
    {
        "ConditionalFormattingOptions": Sequence[TableConditionalFormattingOptionTypeDef],
    },
    total=False,
)

_RequiredUniqueValuesComputationTypeDef = TypedDict(
    "_RequiredUniqueValuesComputationTypeDef",
    {
        "ComputationId": str,
        "Category": DimensionFieldTypeDef,
    },
)
_OptionalUniqueValuesComputationTypeDef = TypedDict(
    "_OptionalUniqueValuesComputationTypeDef",
    {
        "Name": str,
    },
    total=False,
)


class UniqueValuesComputationTypeDef(
    _RequiredUniqueValuesComputationTypeDef, _OptionalUniqueValuesComputationTypeDef
):
    pass


BarChartAggregatedFieldWellsTypeDef = TypedDict(
    "BarChartAggregatedFieldWellsTypeDef",
    {
        "Category": Sequence[DimensionFieldTypeDef],
        "Values": Sequence[MeasureFieldTypeDef],
        "Colors": Sequence[DimensionFieldTypeDef],
        "SmallMultiples": Sequence[DimensionFieldTypeDef],
    },
    total=False,
)

BoxPlotAggregatedFieldWellsTypeDef = TypedDict(
    "BoxPlotAggregatedFieldWellsTypeDef",
    {
        "GroupBy": Sequence[DimensionFieldTypeDef],
        "Values": Sequence[MeasureFieldTypeDef],
    },
    total=False,
)

ComboChartAggregatedFieldWellsTypeDef = TypedDict(
    "ComboChartAggregatedFieldWellsTypeDef",
    {
        "Category": Sequence[DimensionFieldTypeDef],
        "BarValues": Sequence[MeasureFieldTypeDef],
        "Colors": Sequence[DimensionFieldTypeDef],
        "LineValues": Sequence[MeasureFieldTypeDef],
    },
    total=False,
)

FilledMapAggregatedFieldWellsTypeDef = TypedDict(
    "FilledMapAggregatedFieldWellsTypeDef",
    {
        "Geospatial": Sequence[DimensionFieldTypeDef],
        "Values": Sequence[MeasureFieldTypeDef],
    },
    total=False,
)

_RequiredForecastComputationTypeDef = TypedDict(
    "_RequiredForecastComputationTypeDef",
    {
        "ComputationId": str,
        "Time": DimensionFieldTypeDef,
    },
)
_OptionalForecastComputationTypeDef = TypedDict(
    "_OptionalForecastComputationTypeDef",
    {
        "Name": str,
        "Value": MeasureFieldTypeDef,
        "PeriodsForward": int,
        "PeriodsBackward": int,
        "UpperBoundary": float,
        "LowerBoundary": float,
        "PredictionInterval": int,
        "Seasonality": ForecastComputationSeasonalityType,
        "CustomSeasonalityValue": int,
    },
    total=False,
)


class ForecastComputationTypeDef(
    _RequiredForecastComputationTypeDef, _OptionalForecastComputationTypeDef
):
    pass


FunnelChartAggregatedFieldWellsTypeDef = TypedDict(
    "FunnelChartAggregatedFieldWellsTypeDef",
    {
        "Category": Sequence[DimensionFieldTypeDef],
        "Values": Sequence[MeasureFieldTypeDef],
    },
    total=False,
)

GaugeChartFieldWellsTypeDef = TypedDict(
    "GaugeChartFieldWellsTypeDef",
    {
        "Values": Sequence[MeasureFieldTypeDef],
        "TargetValues": Sequence[MeasureFieldTypeDef],
    },
    total=False,
)

GeospatialMapAggregatedFieldWellsTypeDef = TypedDict(
    "GeospatialMapAggregatedFieldWellsTypeDef",
    {
        "Geospatial": Sequence[DimensionFieldTypeDef],
        "Values": Sequence[MeasureFieldTypeDef],
        "Colors": Sequence[DimensionFieldTypeDef],
    },
    total=False,
)

_RequiredGrowthRateComputationTypeDef = TypedDict(
    "_RequiredGrowthRateComputationTypeDef",
    {
        "ComputationId": str,
        "Time": DimensionFieldTypeDef,
    },
)
_OptionalGrowthRateComputationTypeDef = TypedDict(
    "_OptionalGrowthRateComputationTypeDef",
    {
        "Name": str,
        "Value": MeasureFieldTypeDef,
        "PeriodSize": int,
    },
    total=False,
)


class GrowthRateComputationTypeDef(
    _RequiredGrowthRateComputationTypeDef, _OptionalGrowthRateComputationTypeDef
):
    pass


HeatMapAggregatedFieldWellsTypeDef = TypedDict(
    "HeatMapAggregatedFieldWellsTypeDef",
    {
        "Rows": Sequence[DimensionFieldTypeDef],
        "Columns": Sequence[DimensionFieldTypeDef],
        "Values": Sequence[MeasureFieldTypeDef],
    },
    total=False,
)

HistogramAggregatedFieldWellsTypeDef = TypedDict(
    "HistogramAggregatedFieldWellsTypeDef",
    {
        "Values": Sequence[MeasureFieldTypeDef],
    },
    total=False,
)

KPIFieldWellsTypeDef = TypedDict(
    "KPIFieldWellsTypeDef",
    {
        "Values": Sequence[MeasureFieldTypeDef],
        "TargetValues": Sequence[MeasureFieldTypeDef],
        "TrendGroups": Sequence[DimensionFieldTypeDef],
    },
    total=False,
)

LineChartAggregatedFieldWellsTypeDef = TypedDict(
    "LineChartAggregatedFieldWellsTypeDef",
    {
        "Category": Sequence[DimensionFieldTypeDef],
        "Values": Sequence[MeasureFieldTypeDef],
        "Colors": Sequence[DimensionFieldTypeDef],
        "SmallMultiples": Sequence[DimensionFieldTypeDef],
    },
    total=False,
)

_RequiredMaximumMinimumComputationTypeDef = TypedDict(
    "_RequiredMaximumMinimumComputationTypeDef",
    {
        "ComputationId": str,
        "Time": DimensionFieldTypeDef,
        "Type": MaximumMinimumComputationTypeType,
    },
)
_OptionalMaximumMinimumComputationTypeDef = TypedDict(
    "_OptionalMaximumMinimumComputationTypeDef",
    {
        "Name": str,
        "Value": MeasureFieldTypeDef,
    },
    total=False,
)


class MaximumMinimumComputationTypeDef(
    _RequiredMaximumMinimumComputationTypeDef, _OptionalMaximumMinimumComputationTypeDef
):
    pass


_RequiredMetricComparisonComputationTypeDef = TypedDict(
    "_RequiredMetricComparisonComputationTypeDef",
    {
        "ComputationId": str,
        "Time": DimensionFieldTypeDef,
        "FromValue": MeasureFieldTypeDef,
        "TargetValue": MeasureFieldTypeDef,
    },
)
_OptionalMetricComparisonComputationTypeDef = TypedDict(
    "_OptionalMetricComparisonComputationTypeDef",
    {
        "Name": str,
    },
    total=False,
)


class MetricComparisonComputationTypeDef(
    _RequiredMetricComparisonComputationTypeDef, _OptionalMetricComparisonComputationTypeDef
):
    pass


_RequiredPeriodOverPeriodComputationTypeDef = TypedDict(
    "_RequiredPeriodOverPeriodComputationTypeDef",
    {
        "ComputationId": str,
        "Time": DimensionFieldTypeDef,
    },
)
_OptionalPeriodOverPeriodComputationTypeDef = TypedDict(
    "_OptionalPeriodOverPeriodComputationTypeDef",
    {
        "Name": str,
        "Value": MeasureFieldTypeDef,
    },
    total=False,
)


class PeriodOverPeriodComputationTypeDef(
    _RequiredPeriodOverPeriodComputationTypeDef, _OptionalPeriodOverPeriodComputationTypeDef
):
    pass


_RequiredPeriodToDateComputationTypeDef = TypedDict(
    "_RequiredPeriodToDateComputationTypeDef",
    {
        "ComputationId": str,
        "Time": DimensionFieldTypeDef,
    },
)
_OptionalPeriodToDateComputationTypeDef = TypedDict(
    "_OptionalPeriodToDateComputationTypeDef",
    {
        "Name": str,
        "Value": MeasureFieldTypeDef,
        "PeriodTimeGranularity": TimeGranularityType,
    },
    total=False,
)


class PeriodToDateComputationTypeDef(
    _RequiredPeriodToDateComputationTypeDef, _OptionalPeriodToDateComputationTypeDef
):
    pass


PieChartAggregatedFieldWellsTypeDef = TypedDict(
    "PieChartAggregatedFieldWellsTypeDef",
    {
        "Category": Sequence[DimensionFieldTypeDef],
        "Values": Sequence[MeasureFieldTypeDef],
        "SmallMultiples": Sequence[DimensionFieldTypeDef],
    },
    total=False,
)

PivotTableAggregatedFieldWellsTypeDef = TypedDict(
    "PivotTableAggregatedFieldWellsTypeDef",
    {
        "Rows": Sequence[DimensionFieldTypeDef],
        "Columns": Sequence[DimensionFieldTypeDef],
        "Values": Sequence[MeasureFieldTypeDef],
    },
    total=False,
)

RadarChartAggregatedFieldWellsTypeDef = TypedDict(
    "RadarChartAggregatedFieldWellsTypeDef",
    {
        "Category": Sequence[DimensionFieldTypeDef],
        "Color": Sequence[DimensionFieldTypeDef],
        "Values": Sequence[MeasureFieldTypeDef],
    },
    total=False,
)

SankeyDiagramAggregatedFieldWellsTypeDef = TypedDict(
    "SankeyDiagramAggregatedFieldWellsTypeDef",
    {
        "Source": Sequence[DimensionFieldTypeDef],
        "Destination": Sequence[DimensionFieldTypeDef],
        "Weight": Sequence[MeasureFieldTypeDef],
    },
    total=False,
)

ScatterPlotCategoricallyAggregatedFieldWellsTypeDef = TypedDict(
    "ScatterPlotCategoricallyAggregatedFieldWellsTypeDef",
    {
        "XAxis": Sequence[MeasureFieldTypeDef],
        "YAxis": Sequence[MeasureFieldTypeDef],
        "Category": Sequence[DimensionFieldTypeDef],
        "Size": Sequence[MeasureFieldTypeDef],
    },
    total=False,
)

ScatterPlotUnaggregatedFieldWellsTypeDef = TypedDict(
    "ScatterPlotUnaggregatedFieldWellsTypeDef",
    {
        "XAxis": Sequence[DimensionFieldTypeDef],
        "YAxis": Sequence[DimensionFieldTypeDef],
        "Size": Sequence[MeasureFieldTypeDef],
    },
    total=False,
)

TableAggregatedFieldWellsTypeDef = TypedDict(
    "TableAggregatedFieldWellsTypeDef",
    {
        "GroupBy": Sequence[DimensionFieldTypeDef],
        "Values": Sequence[MeasureFieldTypeDef],
    },
    total=False,
)

_RequiredTopBottomMoversComputationTypeDef = TypedDict(
    "_RequiredTopBottomMoversComputationTypeDef",
    {
        "ComputationId": str,
        "Time": DimensionFieldTypeDef,
        "Category": DimensionFieldTypeDef,
        "Type": TopBottomComputationTypeType,
    },
)
_OptionalTopBottomMoversComputationTypeDef = TypedDict(
    "_OptionalTopBottomMoversComputationTypeDef",
    {
        "Name": str,
        "Value": MeasureFieldTypeDef,
        "MoverSize": int,
        "SortOrder": TopBottomSortOrderType,
    },
    total=False,
)


class TopBottomMoversComputationTypeDef(
    _RequiredTopBottomMoversComputationTypeDef, _OptionalTopBottomMoversComputationTypeDef
):
    pass


_RequiredTopBottomRankedComputationTypeDef = TypedDict(
    "_RequiredTopBottomRankedComputationTypeDef",
    {
        "ComputationId": str,
        "Category": DimensionFieldTypeDef,
        "Type": TopBottomComputationTypeType,
    },
)
_OptionalTopBottomRankedComputationTypeDef = TypedDict(
    "_OptionalTopBottomRankedComputationTypeDef",
    {
        "Name": str,
        "Value": MeasureFieldTypeDef,
        "ResultSize": int,
    },
    total=False,
)


class TopBottomRankedComputationTypeDef(
    _RequiredTopBottomRankedComputationTypeDef, _OptionalTopBottomRankedComputationTypeDef
):
    pass


_RequiredTotalAggregationComputationTypeDef = TypedDict(
    "_RequiredTotalAggregationComputationTypeDef",
    {
        "ComputationId": str,
        "Value": MeasureFieldTypeDef,
    },
)
_OptionalTotalAggregationComputationTypeDef = TypedDict(
    "_OptionalTotalAggregationComputationTypeDef",
    {
        "Name": str,
    },
    total=False,
)


class TotalAggregationComputationTypeDef(
    _RequiredTotalAggregationComputationTypeDef, _OptionalTotalAggregationComputationTypeDef
):
    pass


TreeMapAggregatedFieldWellsTypeDef = TypedDict(
    "TreeMapAggregatedFieldWellsTypeDef",
    {
        "Groups": Sequence[DimensionFieldTypeDef],
        "Sizes": Sequence[MeasureFieldTypeDef],
        "Colors": Sequence[MeasureFieldTypeDef],
    },
    total=False,
)

WaterfallChartAggregatedFieldWellsTypeDef = TypedDict(
    "WaterfallChartAggregatedFieldWellsTypeDef",
    {
        "Categories": Sequence[DimensionFieldTypeDef],
        "Values": Sequence[MeasureFieldTypeDef],
        "Breakdowns": Sequence[DimensionFieldTypeDef],
    },
    total=False,
)

WordCloudAggregatedFieldWellsTypeDef = TypedDict(
    "WordCloudAggregatedFieldWellsTypeDef",
    {
        "GroupBy": Sequence[DimensionFieldTypeDef],
        "Size": Sequence[MeasureFieldTypeDef],
    },
    total=False,
)

TableUnaggregatedFieldWellsTypeDef = TypedDict(
    "TableUnaggregatedFieldWellsTypeDef",
    {
        "Values": Sequence[UnaggregatedFieldTypeDef],
    },
    total=False,
)

SectionBasedLayoutConfigurationTypeDef = TypedDict(
    "SectionBasedLayoutConfigurationTypeDef",
    {
        "HeaderSections": Sequence[HeaderFooterSectionConfigurationTypeDef],
        "BodySections": Sequence[BodySectionConfigurationTypeDef],
        "FooterSections": Sequence[HeaderFooterSectionConfigurationTypeDef],
        "CanvasSizeOptions": SectionBasedLayoutCanvasSizeOptionsTypeDef,
    },
)

BarChartFieldWellsTypeDef = TypedDict(
    "BarChartFieldWellsTypeDef",
    {
        "BarChartAggregatedFieldWells": BarChartAggregatedFieldWellsTypeDef,
    },
    total=False,
)

BoxPlotFieldWellsTypeDef = TypedDict(
    "BoxPlotFieldWellsTypeDef",
    {
        "BoxPlotAggregatedFieldWells": BoxPlotAggregatedFieldWellsTypeDef,
    },
    total=False,
)

ComboChartFieldWellsTypeDef = TypedDict(
    "ComboChartFieldWellsTypeDef",
    {
        "ComboChartAggregatedFieldWells": ComboChartAggregatedFieldWellsTypeDef,
    },
    total=False,
)

FilledMapFieldWellsTypeDef = TypedDict(
    "FilledMapFieldWellsTypeDef",
    {
        "FilledMapAggregatedFieldWells": FilledMapAggregatedFieldWellsTypeDef,
    },
    total=False,
)

FunnelChartFieldWellsTypeDef = TypedDict(
    "FunnelChartFieldWellsTypeDef",
    {
        "FunnelChartAggregatedFieldWells": FunnelChartAggregatedFieldWellsTypeDef,
    },
    total=False,
)

GaugeChartConfigurationTypeDef = TypedDict(
    "GaugeChartConfigurationTypeDef",
    {
        "FieldWells": GaugeChartFieldWellsTypeDef,
        "GaugeChartOptions": GaugeChartOptionsTypeDef,
        "DataLabels": DataLabelOptionsTypeDef,
        "TooltipOptions": TooltipOptionsTypeDef,
        "VisualPalette": VisualPaletteTypeDef,
    },
    total=False,
)

GeospatialMapFieldWellsTypeDef = TypedDict(
    "GeospatialMapFieldWellsTypeDef",
    {
        "GeospatialMapAggregatedFieldWells": GeospatialMapAggregatedFieldWellsTypeDef,
    },
    total=False,
)

HeatMapFieldWellsTypeDef = TypedDict(
    "HeatMapFieldWellsTypeDef",
    {
        "HeatMapAggregatedFieldWells": HeatMapAggregatedFieldWellsTypeDef,
    },
    total=False,
)

HistogramFieldWellsTypeDef = TypedDict(
    "HistogramFieldWellsTypeDef",
    {
        "HistogramAggregatedFieldWells": HistogramAggregatedFieldWellsTypeDef,
    },
    total=False,
)

KPIConfigurationTypeDef = TypedDict(
    "KPIConfigurationTypeDef",
    {
        "FieldWells": KPIFieldWellsTypeDef,
        "SortConfiguration": KPISortConfigurationTypeDef,
        "KPIOptions": KPIOptionsTypeDef,
    },
    total=False,
)

LineChartFieldWellsTypeDef = TypedDict(
    "LineChartFieldWellsTypeDef",
    {
        "LineChartAggregatedFieldWells": LineChartAggregatedFieldWellsTypeDef,
    },
    total=False,
)

PieChartFieldWellsTypeDef = TypedDict(
    "PieChartFieldWellsTypeDef",
    {
        "PieChartAggregatedFieldWells": PieChartAggregatedFieldWellsTypeDef,
    },
    total=False,
)

PivotTableFieldWellsTypeDef = TypedDict(
    "PivotTableFieldWellsTypeDef",
    {
        "PivotTableAggregatedFieldWells": PivotTableAggregatedFieldWellsTypeDef,
    },
    total=False,
)

RadarChartFieldWellsTypeDef = TypedDict(
    "RadarChartFieldWellsTypeDef",
    {
        "RadarChartAggregatedFieldWells": RadarChartAggregatedFieldWellsTypeDef,
    },
    total=False,
)

SankeyDiagramFieldWellsTypeDef = TypedDict(
    "SankeyDiagramFieldWellsTypeDef",
    {
        "SankeyDiagramAggregatedFieldWells": SankeyDiagramAggregatedFieldWellsTypeDef,
    },
    total=False,
)

ScatterPlotFieldWellsTypeDef = TypedDict(
    "ScatterPlotFieldWellsTypeDef",
    {
        "ScatterPlotCategoricallyAggregatedFieldWells": (
            ScatterPlotCategoricallyAggregatedFieldWellsTypeDef
        ),
        "ScatterPlotUnaggregatedFieldWells": ScatterPlotUnaggregatedFieldWellsTypeDef,
    },
    total=False,
)

ComputationTypeDef = TypedDict(
    "ComputationTypeDef",
    {
        "TopBottomRanked": TopBottomRankedComputationTypeDef,
        "TopBottomMovers": TopBottomMoversComputationTypeDef,
        "TotalAggregation": TotalAggregationComputationTypeDef,
        "MaximumMinimum": MaximumMinimumComputationTypeDef,
        "MetricComparison": MetricComparisonComputationTypeDef,
        "PeriodOverPeriod": PeriodOverPeriodComputationTypeDef,
        "PeriodToDate": PeriodToDateComputationTypeDef,
        "GrowthRate": GrowthRateComputationTypeDef,
        "UniqueValues": UniqueValuesComputationTypeDef,
        "Forecast": ForecastComputationTypeDef,
    },
    total=False,
)

TreeMapFieldWellsTypeDef = TypedDict(
    "TreeMapFieldWellsTypeDef",
    {
        "TreeMapAggregatedFieldWells": TreeMapAggregatedFieldWellsTypeDef,
    },
    total=False,
)

WaterfallChartFieldWellsTypeDef = TypedDict(
    "WaterfallChartFieldWellsTypeDef",
    {
        "WaterfallChartAggregatedFieldWells": WaterfallChartAggregatedFieldWellsTypeDef,
    },
    total=False,
)

WordCloudFieldWellsTypeDef = TypedDict(
    "WordCloudFieldWellsTypeDef",
    {
        "WordCloudAggregatedFieldWells": WordCloudAggregatedFieldWellsTypeDef,
    },
    total=False,
)

TableFieldWellsTypeDef = TypedDict(
    "TableFieldWellsTypeDef",
    {
        "TableAggregatedFieldWells": TableAggregatedFieldWellsTypeDef,
        "TableUnaggregatedFieldWells": TableUnaggregatedFieldWellsTypeDef,
    },
    total=False,
)

LayoutConfigurationTypeDef = TypedDict(
    "LayoutConfigurationTypeDef",
    {
        "GridLayout": GridLayoutConfigurationTypeDef,
        "FreeFormLayout": FreeFormLayoutConfigurationTypeDef,
        "SectionBasedLayout": SectionBasedLayoutConfigurationTypeDef,
    },
    total=False,
)

BarChartConfigurationTypeDef = TypedDict(
    "BarChartConfigurationTypeDef",
    {
        "FieldWells": BarChartFieldWellsTypeDef,
        "SortConfiguration": BarChartSortConfigurationTypeDef,
        "Orientation": BarChartOrientationType,
        "BarsArrangement": BarsArrangementType,
        "VisualPalette": VisualPaletteTypeDef,
        "SmallMultiplesOptions": SmallMultiplesOptionsTypeDef,
        "CategoryAxis": AxisDisplayOptionsTypeDef,
        "CategoryLabelOptions": ChartAxisLabelOptionsTypeDef,
        "ValueAxis": AxisDisplayOptionsTypeDef,
        "ValueLabelOptions": ChartAxisLabelOptionsTypeDef,
        "ColorLabelOptions": ChartAxisLabelOptionsTypeDef,
        "Legend": LegendOptionsTypeDef,
        "DataLabels": DataLabelOptionsTypeDef,
        "Tooltip": TooltipOptionsTypeDef,
        "ReferenceLines": Sequence[ReferenceLineTypeDef],
        "ContributionAnalysisDefaults": Sequence[ContributionAnalysisDefaultTypeDef],
    },
    total=False,
)

BoxPlotChartConfigurationTypeDef = TypedDict(
    "BoxPlotChartConfigurationTypeDef",
    {
        "FieldWells": BoxPlotFieldWellsTypeDef,
        "SortConfiguration": BoxPlotSortConfigurationTypeDef,
        "BoxPlotOptions": BoxPlotOptionsTypeDef,
        "CategoryAxis": AxisDisplayOptionsTypeDef,
        "CategoryLabelOptions": ChartAxisLabelOptionsTypeDef,
        "PrimaryYAxisDisplayOptions": AxisDisplayOptionsTypeDef,
        "PrimaryYAxisLabelOptions": ChartAxisLabelOptionsTypeDef,
        "Legend": LegendOptionsTypeDef,
        "Tooltip": TooltipOptionsTypeDef,
        "ReferenceLines": Sequence[ReferenceLineTypeDef],
        "VisualPalette": VisualPaletteTypeDef,
    },
    total=False,
)

ComboChartConfigurationTypeDef = TypedDict(
    "ComboChartConfigurationTypeDef",
    {
        "FieldWells": ComboChartFieldWellsTypeDef,
        "SortConfiguration": ComboChartSortConfigurationTypeDef,
        "BarsArrangement": BarsArrangementType,
        "CategoryAxis": AxisDisplayOptionsTypeDef,
        "CategoryLabelOptions": ChartAxisLabelOptionsTypeDef,
        "PrimaryYAxisDisplayOptions": AxisDisplayOptionsTypeDef,
        "PrimaryYAxisLabelOptions": ChartAxisLabelOptionsTypeDef,
        "SecondaryYAxisDisplayOptions": AxisDisplayOptionsTypeDef,
        "SecondaryYAxisLabelOptions": ChartAxisLabelOptionsTypeDef,
        "ColorLabelOptions": ChartAxisLabelOptionsTypeDef,
        "Legend": LegendOptionsTypeDef,
        "BarDataLabels": DataLabelOptionsTypeDef,
        "LineDataLabels": DataLabelOptionsTypeDef,
        "Tooltip": TooltipOptionsTypeDef,
        "ReferenceLines": Sequence[ReferenceLineTypeDef],
        "VisualPalette": VisualPaletteTypeDef,
    },
    total=False,
)

FilledMapConfigurationTypeDef = TypedDict(
    "FilledMapConfigurationTypeDef",
    {
        "FieldWells": FilledMapFieldWellsTypeDef,
        "SortConfiguration": FilledMapSortConfigurationTypeDef,
        "Legend": LegendOptionsTypeDef,
        "Tooltip": TooltipOptionsTypeDef,
        "WindowOptions": GeospatialWindowOptionsTypeDef,
        "MapStyleOptions": GeospatialMapStyleOptionsTypeDef,
    },
    total=False,
)

FunnelChartConfigurationTypeDef = TypedDict(
    "FunnelChartConfigurationTypeDef",
    {
        "FieldWells": FunnelChartFieldWellsTypeDef,
        "SortConfiguration": FunnelChartSortConfigurationTypeDef,
        "CategoryLabelOptions": ChartAxisLabelOptionsTypeDef,
        "ValueLabelOptions": ChartAxisLabelOptionsTypeDef,
        "Tooltip": TooltipOptionsTypeDef,
        "DataLabelOptions": FunnelChartDataLabelOptionsTypeDef,
        "VisualPalette": VisualPaletteTypeDef,
    },
    total=False,
)

_RequiredGaugeChartVisualTypeDef = TypedDict(
    "_RequiredGaugeChartVisualTypeDef",
    {
        "VisualId": str,
    },
)
_OptionalGaugeChartVisualTypeDef = TypedDict(
    "_OptionalGaugeChartVisualTypeDef",
    {
        "Title": VisualTitleLabelOptionsTypeDef,
        "Subtitle": VisualSubtitleLabelOptionsTypeDef,
        "ChartConfiguration": GaugeChartConfigurationTypeDef,
        "ConditionalFormatting": GaugeChartConditionalFormattingTypeDef,
        "Actions": Sequence[VisualCustomActionTypeDef],
    },
    total=False,
)


class GaugeChartVisualTypeDef(_RequiredGaugeChartVisualTypeDef, _OptionalGaugeChartVisualTypeDef):
    pass


GeospatialMapConfigurationTypeDef = TypedDict(
    "GeospatialMapConfigurationTypeDef",
    {
        "FieldWells": GeospatialMapFieldWellsTypeDef,
        "Legend": LegendOptionsTypeDef,
        "Tooltip": TooltipOptionsTypeDef,
        "WindowOptions": GeospatialWindowOptionsTypeDef,
        "MapStyleOptions": GeospatialMapStyleOptionsTypeDef,
        "PointStyleOptions": GeospatialPointStyleOptionsTypeDef,
        "VisualPalette": VisualPaletteTypeDef,
    },
    total=False,
)

HeatMapConfigurationTypeDef = TypedDict(
    "HeatMapConfigurationTypeDef",
    {
        "FieldWells": HeatMapFieldWellsTypeDef,
        "SortConfiguration": HeatMapSortConfigurationTypeDef,
        "RowLabelOptions": ChartAxisLabelOptionsTypeDef,
        "ColumnLabelOptions": ChartAxisLabelOptionsTypeDef,
        "ColorScale": ColorScaleTypeDef,
        "Legend": LegendOptionsTypeDef,
        "DataLabels": DataLabelOptionsTypeDef,
        "Tooltip": TooltipOptionsTypeDef,
    },
    total=False,
)

HistogramConfigurationTypeDef = TypedDict(
    "HistogramConfigurationTypeDef",
    {
        "FieldWells": HistogramFieldWellsTypeDef,
        "XAxisDisplayOptions": AxisDisplayOptionsTypeDef,
        "XAxisLabelOptions": ChartAxisLabelOptionsTypeDef,
        "YAxisDisplayOptions": AxisDisplayOptionsTypeDef,
        "BinOptions": HistogramBinOptionsTypeDef,
        "DataLabels": DataLabelOptionsTypeDef,
        "Tooltip": TooltipOptionsTypeDef,
        "VisualPalette": VisualPaletteTypeDef,
    },
    total=False,
)

_RequiredKPIVisualTypeDef = TypedDict(
    "_RequiredKPIVisualTypeDef",
    {
        "VisualId": str,
    },
)
_OptionalKPIVisualTypeDef = TypedDict(
    "_OptionalKPIVisualTypeDef",
    {
        "Title": VisualTitleLabelOptionsTypeDef,
        "Subtitle": VisualSubtitleLabelOptionsTypeDef,
        "ChartConfiguration": KPIConfigurationTypeDef,
        "ConditionalFormatting": KPIConditionalFormattingTypeDef,
        "Actions": Sequence[VisualCustomActionTypeDef],
        "ColumnHierarchies": Sequence[ColumnHierarchyTypeDef],
    },
    total=False,
)


class KPIVisualTypeDef(_RequiredKPIVisualTypeDef, _OptionalKPIVisualTypeDef):
    pass


LineChartConfigurationTypeDef = TypedDict(
    "LineChartConfigurationTypeDef",
    {
        "FieldWells": LineChartFieldWellsTypeDef,
        "SortConfiguration": LineChartSortConfigurationTypeDef,
        "ForecastConfigurations": Sequence[ForecastConfigurationTypeDef],
        "Type": LineChartTypeType,
        "SmallMultiplesOptions": SmallMultiplesOptionsTypeDef,
        "XAxisDisplayOptions": AxisDisplayOptionsTypeDef,
        "XAxisLabelOptions": ChartAxisLabelOptionsTypeDef,
        "PrimaryYAxisDisplayOptions": LineSeriesAxisDisplayOptionsTypeDef,
        "PrimaryYAxisLabelOptions": ChartAxisLabelOptionsTypeDef,
        "SecondaryYAxisDisplayOptions": LineSeriesAxisDisplayOptionsTypeDef,
        "SecondaryYAxisLabelOptions": ChartAxisLabelOptionsTypeDef,
        "DefaultSeriesSettings": LineChartDefaultSeriesSettingsTypeDef,
        "Series": Sequence[SeriesItemTypeDef],
        "Legend": LegendOptionsTypeDef,
        "DataLabels": DataLabelOptionsTypeDef,
        "ReferenceLines": Sequence[ReferenceLineTypeDef],
        "Tooltip": TooltipOptionsTypeDef,
        "ContributionAnalysisDefaults": Sequence[ContributionAnalysisDefaultTypeDef],
        "VisualPalette": VisualPaletteTypeDef,
    },
    total=False,
)

PieChartConfigurationTypeDef = TypedDict(
    "PieChartConfigurationTypeDef",
    {
        "FieldWells": PieChartFieldWellsTypeDef,
        "SortConfiguration": PieChartSortConfigurationTypeDef,
        "DonutOptions": DonutOptionsTypeDef,
        "SmallMultiplesOptions": SmallMultiplesOptionsTypeDef,
        "CategoryLabelOptions": ChartAxisLabelOptionsTypeDef,
        "ValueLabelOptions": ChartAxisLabelOptionsTypeDef,
        "Legend": LegendOptionsTypeDef,
        "DataLabels": DataLabelOptionsTypeDef,
        "Tooltip": TooltipOptionsTypeDef,
        "VisualPalette": VisualPaletteTypeDef,
        "ContributionAnalysisDefaults": Sequence[ContributionAnalysisDefaultTypeDef],
    },
    total=False,
)

PivotTableConfigurationTypeDef = TypedDict(
    "PivotTableConfigurationTypeDef",
    {
        "FieldWells": PivotTableFieldWellsTypeDef,
        "SortConfiguration": PivotTableSortConfigurationTypeDef,
        "TableOptions": PivotTableOptionsTypeDef,
        "TotalOptions": PivotTableTotalOptionsTypeDef,
        "FieldOptions": PivotTableFieldOptionsTypeDef,
        "PaginatedReportOptions": PivotTablePaginatedReportOptionsTypeDef,
    },
    total=False,
)

RadarChartConfigurationTypeDef = TypedDict(
    "RadarChartConfigurationTypeDef",
    {
        "FieldWells": RadarChartFieldWellsTypeDef,
        "SortConfiguration": RadarChartSortConfigurationTypeDef,
        "Shape": RadarChartShapeType,
        "BaseSeriesSettings": RadarChartSeriesSettingsTypeDef,
        "StartAngle": float,
        "VisualPalette": VisualPaletteTypeDef,
        "AlternateBandColorsVisibility": VisibilityType,
        "AlternateBandEvenColor": str,
        "AlternateBandOddColor": str,
        "CategoryAxis": AxisDisplayOptionsTypeDef,
        "CategoryLabelOptions": ChartAxisLabelOptionsTypeDef,
        "ColorAxis": AxisDisplayOptionsTypeDef,
        "ColorLabelOptions": ChartAxisLabelOptionsTypeDef,
        "Legend": LegendOptionsTypeDef,
    },
    total=False,
)

SankeyDiagramChartConfigurationTypeDef = TypedDict(
    "SankeyDiagramChartConfigurationTypeDef",
    {
        "FieldWells": SankeyDiagramFieldWellsTypeDef,
        "SortConfiguration": SankeyDiagramSortConfigurationTypeDef,
        "DataLabels": DataLabelOptionsTypeDef,
    },
    total=False,
)

ScatterPlotConfigurationTypeDef = TypedDict(
    "ScatterPlotConfigurationTypeDef",
    {
        "FieldWells": ScatterPlotFieldWellsTypeDef,
        "XAxisLabelOptions": ChartAxisLabelOptionsTypeDef,
        "XAxisDisplayOptions": AxisDisplayOptionsTypeDef,
        "YAxisLabelOptions": ChartAxisLabelOptionsTypeDef,
        "YAxisDisplayOptions": AxisDisplayOptionsTypeDef,
        "Legend": LegendOptionsTypeDef,
        "DataLabels": DataLabelOptionsTypeDef,
        "Tooltip": TooltipOptionsTypeDef,
        "VisualPalette": VisualPaletteTypeDef,
    },
    total=False,
)

InsightConfigurationTypeDef = TypedDict(
    "InsightConfigurationTypeDef",
    {
        "Computations": Sequence[ComputationTypeDef],
        "CustomNarrative": CustomNarrativeOptionsTypeDef,
    },
    total=False,
)

TreeMapConfigurationTypeDef = TypedDict(
    "TreeMapConfigurationTypeDef",
    {
        "FieldWells": TreeMapFieldWellsTypeDef,
        "SortConfiguration": TreeMapSortConfigurationTypeDef,
        "GroupLabelOptions": ChartAxisLabelOptionsTypeDef,
        "SizeLabelOptions": ChartAxisLabelOptionsTypeDef,
        "ColorLabelOptions": ChartAxisLabelOptionsTypeDef,
        "ColorScale": ColorScaleTypeDef,
        "Legend": LegendOptionsTypeDef,
        "DataLabels": DataLabelOptionsTypeDef,
        "Tooltip": TooltipOptionsTypeDef,
    },
    total=False,
)

WaterfallChartConfigurationTypeDef = TypedDict(
    "WaterfallChartConfigurationTypeDef",
    {
        "FieldWells": WaterfallChartFieldWellsTypeDef,
        "SortConfiguration": WaterfallChartSortConfigurationTypeDef,
        "WaterfallChartOptions": WaterfallChartOptionsTypeDef,
        "CategoryAxisLabelOptions": ChartAxisLabelOptionsTypeDef,
        "CategoryAxisDisplayOptions": AxisDisplayOptionsTypeDef,
        "PrimaryYAxisLabelOptions": ChartAxisLabelOptionsTypeDef,
        "PrimaryYAxisDisplayOptions": AxisDisplayOptionsTypeDef,
        "Legend": LegendOptionsTypeDef,
        "DataLabels": DataLabelOptionsTypeDef,
        "VisualPalette": VisualPaletteTypeDef,
    },
    total=False,
)

WordCloudChartConfigurationTypeDef = TypedDict(
    "WordCloudChartConfigurationTypeDef",
    {
        "FieldWells": WordCloudFieldWellsTypeDef,
        "SortConfiguration": WordCloudSortConfigurationTypeDef,
        "CategoryLabelOptions": ChartAxisLabelOptionsTypeDef,
        "WordCloudOptions": WordCloudOptionsTypeDef,
    },
    total=False,
)

TableConfigurationTypeDef = TypedDict(
    "TableConfigurationTypeDef",
    {
        "FieldWells": TableFieldWellsTypeDef,
        "SortConfiguration": TableSortConfigurationTypeDef,
        "TableOptions": TableOptionsTypeDef,
        "TotalOptions": TotalOptionsTypeDef,
        "FieldOptions": TableFieldOptionsTypeDef,
        "PaginatedReportOptions": TablePaginatedReportOptionsTypeDef,
        "TableInlineVisualizations": Sequence[TableInlineVisualizationTypeDef],
    },
    total=False,
)

LayoutTypeDef = TypedDict(
    "LayoutTypeDef",
    {
        "Configuration": LayoutConfigurationTypeDef,
    },
)

_RequiredBarChartVisualTypeDef = TypedDict(
    "_RequiredBarChartVisualTypeDef",
    {
        "VisualId": str,
    },
)
_OptionalBarChartVisualTypeDef = TypedDict(
    "_OptionalBarChartVisualTypeDef",
    {
        "Title": VisualTitleLabelOptionsTypeDef,
        "Subtitle": VisualSubtitleLabelOptionsTypeDef,
        "ChartConfiguration": BarChartConfigurationTypeDef,
        "Actions": Sequence[VisualCustomActionTypeDef],
        "ColumnHierarchies": Sequence[ColumnHierarchyTypeDef],
    },
    total=False,
)


class BarChartVisualTypeDef(_RequiredBarChartVisualTypeDef, _OptionalBarChartVisualTypeDef):
    pass


_RequiredBoxPlotVisualTypeDef = TypedDict(
    "_RequiredBoxPlotVisualTypeDef",
    {
        "VisualId": str,
    },
)
_OptionalBoxPlotVisualTypeDef = TypedDict(
    "_OptionalBoxPlotVisualTypeDef",
    {
        "Title": VisualTitleLabelOptionsTypeDef,
        "Subtitle": VisualSubtitleLabelOptionsTypeDef,
        "ChartConfiguration": BoxPlotChartConfigurationTypeDef,
        "Actions": Sequence[VisualCustomActionTypeDef],
        "ColumnHierarchies": Sequence[ColumnHierarchyTypeDef],
    },
    total=False,
)


class BoxPlotVisualTypeDef(_RequiredBoxPlotVisualTypeDef, _OptionalBoxPlotVisualTypeDef):
    pass


_RequiredComboChartVisualTypeDef = TypedDict(
    "_RequiredComboChartVisualTypeDef",
    {
        "VisualId": str,
    },
)
_OptionalComboChartVisualTypeDef = TypedDict(
    "_OptionalComboChartVisualTypeDef",
    {
        "Title": VisualTitleLabelOptionsTypeDef,
        "Subtitle": VisualSubtitleLabelOptionsTypeDef,
        "ChartConfiguration": ComboChartConfigurationTypeDef,
        "Actions": Sequence[VisualCustomActionTypeDef],
        "ColumnHierarchies": Sequence[ColumnHierarchyTypeDef],
    },
    total=False,
)


class ComboChartVisualTypeDef(_RequiredComboChartVisualTypeDef, _OptionalComboChartVisualTypeDef):
    pass


_RequiredFilledMapVisualTypeDef = TypedDict(
    "_RequiredFilledMapVisualTypeDef",
    {
        "VisualId": str,
    },
)
_OptionalFilledMapVisualTypeDef = TypedDict(
    "_OptionalFilledMapVisualTypeDef",
    {
        "Title": VisualTitleLabelOptionsTypeDef,
        "Subtitle": VisualSubtitleLabelOptionsTypeDef,
        "ChartConfiguration": FilledMapConfigurationTypeDef,
        "ConditionalFormatting": FilledMapConditionalFormattingTypeDef,
        "ColumnHierarchies": Sequence[ColumnHierarchyTypeDef],
        "Actions": Sequence[VisualCustomActionTypeDef],
    },
    total=False,
)


class FilledMapVisualTypeDef(_RequiredFilledMapVisualTypeDef, _OptionalFilledMapVisualTypeDef):
    pass


_RequiredFunnelChartVisualTypeDef = TypedDict(
    "_RequiredFunnelChartVisualTypeDef",
    {
        "VisualId": str,
    },
)
_OptionalFunnelChartVisualTypeDef = TypedDict(
    "_OptionalFunnelChartVisualTypeDef",
    {
        "Title": VisualTitleLabelOptionsTypeDef,
        "Subtitle": VisualSubtitleLabelOptionsTypeDef,
        "ChartConfiguration": FunnelChartConfigurationTypeDef,
        "Actions": Sequence[VisualCustomActionTypeDef],
        "ColumnHierarchies": Sequence[ColumnHierarchyTypeDef],
    },
    total=False,
)


class FunnelChartVisualTypeDef(
    _RequiredFunnelChartVisualTypeDef, _OptionalFunnelChartVisualTypeDef
):
    pass


_RequiredGeospatialMapVisualTypeDef = TypedDict(
    "_RequiredGeospatialMapVisualTypeDef",
    {
        "VisualId": str,
    },
)
_OptionalGeospatialMapVisualTypeDef = TypedDict(
    "_OptionalGeospatialMapVisualTypeDef",
    {
        "Title": VisualTitleLabelOptionsTypeDef,
        "Subtitle": VisualSubtitleLabelOptionsTypeDef,
        "ChartConfiguration": GeospatialMapConfigurationTypeDef,
        "ColumnHierarchies": Sequence[ColumnHierarchyTypeDef],
        "Actions": Sequence[VisualCustomActionTypeDef],
    },
    total=False,
)


class GeospatialMapVisualTypeDef(
    _RequiredGeospatialMapVisualTypeDef, _OptionalGeospatialMapVisualTypeDef
):
    pass


_RequiredHeatMapVisualTypeDef = TypedDict(
    "_RequiredHeatMapVisualTypeDef",
    {
        "VisualId": str,
    },
)
_OptionalHeatMapVisualTypeDef = TypedDict(
    "_OptionalHeatMapVisualTypeDef",
    {
        "Title": VisualTitleLabelOptionsTypeDef,
        "Subtitle": VisualSubtitleLabelOptionsTypeDef,
        "ChartConfiguration": HeatMapConfigurationTypeDef,
        "ColumnHierarchies": Sequence[ColumnHierarchyTypeDef],
        "Actions": Sequence[VisualCustomActionTypeDef],
    },
    total=False,
)


class HeatMapVisualTypeDef(_RequiredHeatMapVisualTypeDef, _OptionalHeatMapVisualTypeDef):
    pass


_RequiredHistogramVisualTypeDef = TypedDict(
    "_RequiredHistogramVisualTypeDef",
    {
        "VisualId": str,
    },
)
_OptionalHistogramVisualTypeDef = TypedDict(
    "_OptionalHistogramVisualTypeDef",
    {
        "Title": VisualTitleLabelOptionsTypeDef,
        "Subtitle": VisualSubtitleLabelOptionsTypeDef,
        "ChartConfiguration": HistogramConfigurationTypeDef,
        "Actions": Sequence[VisualCustomActionTypeDef],
    },
    total=False,
)


class HistogramVisualTypeDef(_RequiredHistogramVisualTypeDef, _OptionalHistogramVisualTypeDef):
    pass


_RequiredLineChartVisualTypeDef = TypedDict(
    "_RequiredLineChartVisualTypeDef",
    {
        "VisualId": str,
    },
)
_OptionalLineChartVisualTypeDef = TypedDict(
    "_OptionalLineChartVisualTypeDef",
    {
        "Title": VisualTitleLabelOptionsTypeDef,
        "Subtitle": VisualSubtitleLabelOptionsTypeDef,
        "ChartConfiguration": LineChartConfigurationTypeDef,
        "Actions": Sequence[VisualCustomActionTypeDef],
        "ColumnHierarchies": Sequence[ColumnHierarchyTypeDef],
    },
    total=False,
)


class LineChartVisualTypeDef(_RequiredLineChartVisualTypeDef, _OptionalLineChartVisualTypeDef):
    pass


_RequiredPieChartVisualTypeDef = TypedDict(
    "_RequiredPieChartVisualTypeDef",
    {
        "VisualId": str,
    },
)
_OptionalPieChartVisualTypeDef = TypedDict(
    "_OptionalPieChartVisualTypeDef",
    {
        "Title": VisualTitleLabelOptionsTypeDef,
        "Subtitle": VisualSubtitleLabelOptionsTypeDef,
        "ChartConfiguration": PieChartConfigurationTypeDef,
        "Actions": Sequence[VisualCustomActionTypeDef],
        "ColumnHierarchies": Sequence[ColumnHierarchyTypeDef],
    },
    total=False,
)


class PieChartVisualTypeDef(_RequiredPieChartVisualTypeDef, _OptionalPieChartVisualTypeDef):
    pass


_RequiredPivotTableVisualTypeDef = TypedDict(
    "_RequiredPivotTableVisualTypeDef",
    {
        "VisualId": str,
    },
)
_OptionalPivotTableVisualTypeDef = TypedDict(
    "_OptionalPivotTableVisualTypeDef",
    {
        "Title": VisualTitleLabelOptionsTypeDef,
        "Subtitle": VisualSubtitleLabelOptionsTypeDef,
        "ChartConfiguration": PivotTableConfigurationTypeDef,
        "ConditionalFormatting": PivotTableConditionalFormattingTypeDef,
        "Actions": Sequence[VisualCustomActionTypeDef],
    },
    total=False,
)


class PivotTableVisualTypeDef(_RequiredPivotTableVisualTypeDef, _OptionalPivotTableVisualTypeDef):
    pass


_RequiredRadarChartVisualTypeDef = TypedDict(
    "_RequiredRadarChartVisualTypeDef",
    {
        "VisualId": str,
    },
)
_OptionalRadarChartVisualTypeDef = TypedDict(
    "_OptionalRadarChartVisualTypeDef",
    {
        "Title": VisualTitleLabelOptionsTypeDef,
        "Subtitle": VisualSubtitleLabelOptionsTypeDef,
        "ChartConfiguration": RadarChartConfigurationTypeDef,
        "Actions": Sequence[VisualCustomActionTypeDef],
        "ColumnHierarchies": Sequence[ColumnHierarchyTypeDef],
    },
    total=False,
)


class RadarChartVisualTypeDef(_RequiredRadarChartVisualTypeDef, _OptionalRadarChartVisualTypeDef):
    pass


_RequiredSankeyDiagramVisualTypeDef = TypedDict(
    "_RequiredSankeyDiagramVisualTypeDef",
    {
        "VisualId": str,
    },
)
_OptionalSankeyDiagramVisualTypeDef = TypedDict(
    "_OptionalSankeyDiagramVisualTypeDef",
    {
        "Title": VisualTitleLabelOptionsTypeDef,
        "Subtitle": VisualSubtitleLabelOptionsTypeDef,
        "ChartConfiguration": SankeyDiagramChartConfigurationTypeDef,
        "Actions": Sequence[VisualCustomActionTypeDef],
    },
    total=False,
)


class SankeyDiagramVisualTypeDef(
    _RequiredSankeyDiagramVisualTypeDef, _OptionalSankeyDiagramVisualTypeDef
):
    pass


_RequiredScatterPlotVisualTypeDef = TypedDict(
    "_RequiredScatterPlotVisualTypeDef",
    {
        "VisualId": str,
    },
)
_OptionalScatterPlotVisualTypeDef = TypedDict(
    "_OptionalScatterPlotVisualTypeDef",
    {
        "Title": VisualTitleLabelOptionsTypeDef,
        "Subtitle": VisualSubtitleLabelOptionsTypeDef,
        "ChartConfiguration": ScatterPlotConfigurationTypeDef,
        "Actions": Sequence[VisualCustomActionTypeDef],
        "ColumnHierarchies": Sequence[ColumnHierarchyTypeDef],
    },
    total=False,
)


class ScatterPlotVisualTypeDef(
    _RequiredScatterPlotVisualTypeDef, _OptionalScatterPlotVisualTypeDef
):
    pass


_RequiredInsightVisualTypeDef = TypedDict(
    "_RequiredInsightVisualTypeDef",
    {
        "VisualId": str,
        "DataSetIdentifier": str,
    },
)
_OptionalInsightVisualTypeDef = TypedDict(
    "_OptionalInsightVisualTypeDef",
    {
        "Title": VisualTitleLabelOptionsTypeDef,
        "Subtitle": VisualSubtitleLabelOptionsTypeDef,
        "InsightConfiguration": InsightConfigurationTypeDef,
        "Actions": Sequence[VisualCustomActionTypeDef],
    },
    total=False,
)


class InsightVisualTypeDef(_RequiredInsightVisualTypeDef, _OptionalInsightVisualTypeDef):
    pass


_RequiredTreeMapVisualTypeDef = TypedDict(
    "_RequiredTreeMapVisualTypeDef",
    {
        "VisualId": str,
    },
)
_OptionalTreeMapVisualTypeDef = TypedDict(
    "_OptionalTreeMapVisualTypeDef",
    {
        "Title": VisualTitleLabelOptionsTypeDef,
        "Subtitle": VisualSubtitleLabelOptionsTypeDef,
        "ChartConfiguration": TreeMapConfigurationTypeDef,
        "Actions": Sequence[VisualCustomActionTypeDef],
        "ColumnHierarchies": Sequence[ColumnHierarchyTypeDef],
    },
    total=False,
)


class TreeMapVisualTypeDef(_RequiredTreeMapVisualTypeDef, _OptionalTreeMapVisualTypeDef):
    pass


_RequiredWaterfallVisualTypeDef = TypedDict(
    "_RequiredWaterfallVisualTypeDef",
    {
        "VisualId": str,
    },
)
_OptionalWaterfallVisualTypeDef = TypedDict(
    "_OptionalWaterfallVisualTypeDef",
    {
        "Title": VisualTitleLabelOptionsTypeDef,
        "Subtitle": VisualSubtitleLabelOptionsTypeDef,
        "ChartConfiguration": WaterfallChartConfigurationTypeDef,
        "Actions": Sequence[VisualCustomActionTypeDef],
        "ColumnHierarchies": Sequence[ColumnHierarchyTypeDef],
    },
    total=False,
)


class WaterfallVisualTypeDef(_RequiredWaterfallVisualTypeDef, _OptionalWaterfallVisualTypeDef):
    pass


_RequiredWordCloudVisualTypeDef = TypedDict(
    "_RequiredWordCloudVisualTypeDef",
    {
        "VisualId": str,
    },
)
_OptionalWordCloudVisualTypeDef = TypedDict(
    "_OptionalWordCloudVisualTypeDef",
    {
        "Title": VisualTitleLabelOptionsTypeDef,
        "Subtitle": VisualSubtitleLabelOptionsTypeDef,
        "ChartConfiguration": WordCloudChartConfigurationTypeDef,
        "Actions": Sequence[VisualCustomActionTypeDef],
        "ColumnHierarchies": Sequence[ColumnHierarchyTypeDef],
    },
    total=False,
)


class WordCloudVisualTypeDef(_RequiredWordCloudVisualTypeDef, _OptionalWordCloudVisualTypeDef):
    pass


_RequiredTableVisualTypeDef = TypedDict(
    "_RequiredTableVisualTypeDef",
    {
        "VisualId": str,
    },
)
_OptionalTableVisualTypeDef = TypedDict(
    "_OptionalTableVisualTypeDef",
    {
        "Title": VisualTitleLabelOptionsTypeDef,
        "Subtitle": VisualSubtitleLabelOptionsTypeDef,
        "ChartConfiguration": TableConfigurationTypeDef,
        "ConditionalFormatting": TableConditionalFormattingTypeDef,
        "Actions": Sequence[VisualCustomActionTypeDef],
    },
    total=False,
)


class TableVisualTypeDef(_RequiredTableVisualTypeDef, _OptionalTableVisualTypeDef):
    pass


VisualTypeDef = TypedDict(
    "VisualTypeDef",
    {
        "TableVisual": TableVisualTypeDef,
        "PivotTableVisual": PivotTableVisualTypeDef,
        "BarChartVisual": BarChartVisualTypeDef,
        "KPIVisual": KPIVisualTypeDef,
        "PieChartVisual": PieChartVisualTypeDef,
        "GaugeChartVisual": GaugeChartVisualTypeDef,
        "LineChartVisual": LineChartVisualTypeDef,
        "HeatMapVisual": HeatMapVisualTypeDef,
        "TreeMapVisual": TreeMapVisualTypeDef,
        "GeospatialMapVisual": GeospatialMapVisualTypeDef,
        "FilledMapVisual": FilledMapVisualTypeDef,
        "FunnelChartVisual": FunnelChartVisualTypeDef,
        "ScatterPlotVisual": ScatterPlotVisualTypeDef,
        "ComboChartVisual": ComboChartVisualTypeDef,
        "BoxPlotVisual": BoxPlotVisualTypeDef,
        "WaterfallVisual": WaterfallVisualTypeDef,
        "HistogramVisual": HistogramVisualTypeDef,
        "WordCloudVisual": WordCloudVisualTypeDef,
        "InsightVisual": InsightVisualTypeDef,
        "SankeyDiagramVisual": SankeyDiagramVisualTypeDef,
        "CustomContentVisual": CustomContentVisualTypeDef,
        "EmptyVisual": EmptyVisualTypeDef,
        "RadarChartVisual": RadarChartVisualTypeDef,
    },
    total=False,
)

_RequiredSheetDefinitionTypeDef = TypedDict(
    "_RequiredSheetDefinitionTypeDef",
    {
        "SheetId": str,
    },
)
_OptionalSheetDefinitionTypeDef = TypedDict(
    "_OptionalSheetDefinitionTypeDef",
    {
        "Title": str,
        "Description": str,
        "Name": str,
        "ParameterControls": Sequence[ParameterControlTypeDef],
        "FilterControls": Sequence[FilterControlTypeDef],
        "Visuals": Sequence[VisualTypeDef],
        "TextBoxes": Sequence[SheetTextBoxTypeDef],
        "Layouts": Sequence[LayoutTypeDef],
        "SheetControlLayouts": Sequence[SheetControlLayoutTypeDef],
        "ContentType": SheetContentTypeType,
    },
    total=False,
)


class SheetDefinitionTypeDef(_RequiredSheetDefinitionTypeDef, _OptionalSheetDefinitionTypeDef):
    pass


_RequiredAnalysisDefinitionTypeDef = TypedDict(
    "_RequiredAnalysisDefinitionTypeDef",
    {
        "DataSetIdentifierDeclarations": Sequence[DataSetIdentifierDeclarationTypeDef],
    },
)
_OptionalAnalysisDefinitionTypeDef = TypedDict(
    "_OptionalAnalysisDefinitionTypeDef",
    {
        "Sheets": Sequence[SheetDefinitionTypeDef],
        "CalculatedFields": Sequence[CalculatedFieldTypeDef],
        "ParameterDeclarations": Sequence[ParameterDeclarationTypeDef],
        "FilterGroups": Sequence[FilterGroupTypeDef],
        "ColumnConfigurations": Sequence[ColumnConfigurationTypeDef],
        "AnalysisDefaults": AnalysisDefaultsTypeDef,
    },
    total=False,
)


class AnalysisDefinitionTypeDef(
    _RequiredAnalysisDefinitionTypeDef, _OptionalAnalysisDefinitionTypeDef
):
    pass


_RequiredDashboardVersionDefinitionTypeDef = TypedDict(
    "_RequiredDashboardVersionDefinitionTypeDef",
    {
        "DataSetIdentifierDeclarations": Sequence[DataSetIdentifierDeclarationTypeDef],
    },
)
_OptionalDashboardVersionDefinitionTypeDef = TypedDict(
    "_OptionalDashboardVersionDefinitionTypeDef",
    {
        "Sheets": Sequence[SheetDefinitionTypeDef],
        "CalculatedFields": Sequence[CalculatedFieldTypeDef],
        "ParameterDeclarations": Sequence[ParameterDeclarationTypeDef],
        "FilterGroups": Sequence[FilterGroupTypeDef],
        "ColumnConfigurations": Sequence[ColumnConfigurationTypeDef],
        "AnalysisDefaults": AnalysisDefaultsTypeDef,
    },
    total=False,
)


class DashboardVersionDefinitionTypeDef(
    _RequiredDashboardVersionDefinitionTypeDef, _OptionalDashboardVersionDefinitionTypeDef
):
    pass


_RequiredTemplateVersionDefinitionTypeDef = TypedDict(
    "_RequiredTemplateVersionDefinitionTypeDef",
    {
        "DataSetConfigurations": Sequence[DataSetConfigurationTypeDef],
    },
)
_OptionalTemplateVersionDefinitionTypeDef = TypedDict(
    "_OptionalTemplateVersionDefinitionTypeDef",
    {
        "Sheets": Sequence[SheetDefinitionTypeDef],
        "CalculatedFields": Sequence[CalculatedFieldTypeDef],
        "ParameterDeclarations": Sequence[ParameterDeclarationTypeDef],
        "FilterGroups": Sequence[FilterGroupTypeDef],
        "ColumnConfigurations": Sequence[ColumnConfigurationTypeDef],
        "AnalysisDefaults": AnalysisDefaultsTypeDef,
    },
    total=False,
)


class TemplateVersionDefinitionTypeDef(
    _RequiredTemplateVersionDefinitionTypeDef, _OptionalTemplateVersionDefinitionTypeDef
):
    pass


_RequiredCreateAnalysisRequestRequestTypeDef = TypedDict(
    "_RequiredCreateAnalysisRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "AnalysisId": str,
        "Name": str,
    },
)
_OptionalCreateAnalysisRequestRequestTypeDef = TypedDict(
    "_OptionalCreateAnalysisRequestRequestTypeDef",
    {
        "Parameters": ParametersTypeDef,
        "Permissions": Sequence[ResourcePermissionTypeDef],
        "SourceEntity": AnalysisSourceEntityTypeDef,
        "ThemeArn": str,
        "Tags": Sequence[TagTypeDef],
        "Definition": AnalysisDefinitionTypeDef,
    },
    total=False,
)


class CreateAnalysisRequestRequestTypeDef(
    _RequiredCreateAnalysisRequestRequestTypeDef, _OptionalCreateAnalysisRequestRequestTypeDef
):
    pass


DescribeAnalysisDefinitionResponseTypeDef = TypedDict(
    "DescribeAnalysisDefinitionResponseTypeDef",
    {
        "AnalysisId": str,
        "Name": str,
        "Errors": List[AnalysisErrorTypeDef],
        "ResourceStatus": ResourceStatusType,
        "ThemeArn": str,
        "Definition": AnalysisDefinitionTypeDef,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdateAnalysisRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateAnalysisRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "AnalysisId": str,
        "Name": str,
    },
)
_OptionalUpdateAnalysisRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateAnalysisRequestRequestTypeDef",
    {
        "Parameters": ParametersTypeDef,
        "SourceEntity": AnalysisSourceEntityTypeDef,
        "ThemeArn": str,
        "Definition": AnalysisDefinitionTypeDef,
    },
    total=False,
)


class UpdateAnalysisRequestRequestTypeDef(
    _RequiredUpdateAnalysisRequestRequestTypeDef, _OptionalUpdateAnalysisRequestRequestTypeDef
):
    pass


_RequiredCreateDashboardRequestRequestTypeDef = TypedDict(
    "_RequiredCreateDashboardRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DashboardId": str,
        "Name": str,
    },
)
_OptionalCreateDashboardRequestRequestTypeDef = TypedDict(
    "_OptionalCreateDashboardRequestRequestTypeDef",
    {
        "Parameters": ParametersTypeDef,
        "Permissions": Sequence[ResourcePermissionTypeDef],
        "SourceEntity": DashboardSourceEntityTypeDef,
        "Tags": Sequence[TagTypeDef],
        "VersionDescription": str,
        "DashboardPublishOptions": DashboardPublishOptionsTypeDef,
        "ThemeArn": str,
        "Definition": DashboardVersionDefinitionTypeDef,
    },
    total=False,
)


class CreateDashboardRequestRequestTypeDef(
    _RequiredCreateDashboardRequestRequestTypeDef, _OptionalCreateDashboardRequestRequestTypeDef
):
    pass


DescribeDashboardDefinitionResponseTypeDef = TypedDict(
    "DescribeDashboardDefinitionResponseTypeDef",
    {
        "DashboardId": str,
        "Errors": List[DashboardErrorTypeDef],
        "Name": str,
        "ResourceStatus": ResourceStatusType,
        "ThemeArn": str,
        "Definition": DashboardVersionDefinitionTypeDef,
        "Status": int,
        "RequestId": str,
        "DashboardPublishOptions": DashboardPublishOptionsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdateDashboardRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateDashboardRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DashboardId": str,
        "Name": str,
    },
)
_OptionalUpdateDashboardRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateDashboardRequestRequestTypeDef",
    {
        "SourceEntity": DashboardSourceEntityTypeDef,
        "Parameters": ParametersTypeDef,
        "VersionDescription": str,
        "DashboardPublishOptions": DashboardPublishOptionsTypeDef,
        "ThemeArn": str,
        "Definition": DashboardVersionDefinitionTypeDef,
    },
    total=False,
)


class UpdateDashboardRequestRequestTypeDef(
    _RequiredUpdateDashboardRequestRequestTypeDef, _OptionalUpdateDashboardRequestRequestTypeDef
):
    pass


_RequiredCreateTemplateRequestRequestTypeDef = TypedDict(
    "_RequiredCreateTemplateRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "TemplateId": str,
    },
)
_OptionalCreateTemplateRequestRequestTypeDef = TypedDict(
    "_OptionalCreateTemplateRequestRequestTypeDef",
    {
        "Name": str,
        "Permissions": Sequence[ResourcePermissionTypeDef],
        "SourceEntity": TemplateSourceEntityTypeDef,
        "Tags": Sequence[TagTypeDef],
        "VersionDescription": str,
        "Definition": TemplateVersionDefinitionTypeDef,
    },
    total=False,
)


class CreateTemplateRequestRequestTypeDef(
    _RequiredCreateTemplateRequestRequestTypeDef, _OptionalCreateTemplateRequestRequestTypeDef
):
    pass


DescribeTemplateDefinitionResponseTypeDef = TypedDict(
    "DescribeTemplateDefinitionResponseTypeDef",
    {
        "Name": str,
        "TemplateId": str,
        "Errors": List[TemplateErrorTypeDef],
        "ResourceStatus": ResourceStatusType,
        "ThemeArn": str,
        "Definition": TemplateVersionDefinitionTypeDef,
        "Status": int,
        "RequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdateTemplateRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateTemplateRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "TemplateId": str,
    },
)
_OptionalUpdateTemplateRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateTemplateRequestRequestTypeDef",
    {
        "SourceEntity": TemplateSourceEntityTypeDef,
        "VersionDescription": str,
        "Name": str,
        "Definition": TemplateVersionDefinitionTypeDef,
    },
    total=False,
)


class UpdateTemplateRequestRequestTypeDef(
    _RequiredUpdateTemplateRequestRequestTypeDef, _OptionalUpdateTemplateRequestRequestTypeDef
):
    pass
