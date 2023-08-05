# -*- coding: utf-8 -*-
"""
urban.vocabulary
------------------

Created by mpeeters
:license: GPL, see LICENCE.txt for more details.
"""

from plone.supermodel import model
from zope import schema
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.interface import Interface
from plone.directives import form
from collective.z3cform.select2.widget.widget import MultiSelect2FieldWidget

from urban.vocabulary import _


class IUrbanVocabularyLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IPCASettings(model.Schema):

    model.fieldset(
        'pca',
        label=_('PCA Vocabulary'),
        fields=[
            'pca_url',
            'pca_boolean_mapping',
            'pca_boolean_mapping_value',
        ],
    )

    pca_url = schema.TextLine(
        title=_(u'URL'),
        description=_(u"The order of the 'att' parameter must be TITLE,KEY"),
        required=True,
    )

    form.widget(pca_boolean_mapping=MultiSelect2FieldWidget)
    pca_boolean_mapping = schema.List(
        title=_(u'Mapping of vocabularies values to boolean'),
        value_type=schema.Choice(
            title=_(u'Value'),
            vocabulary='urban.vocabulary.PCAZones',
        ),
        required=False,
    )

    pca_boolean_mapping_value = schema.Choice(
        title=_(u'Boolean mapping value'),
        values=(True, False),
        required=True,
        default=True,
    )


class INatura2000Settings(model.Schema):

    model.fieldset(
        'natura_2000',
        label=_('Natura 2000 Vocabulary'),
        fields=[
            'natura_2000_url',
            'natura_2000_boolean_mapping',
            'natura_2000_boolean_mapping_value',
        ],
    )

    natura_2000_url = schema.TextLine(
        title=_(u'URL'),
        description=_(u"The order of the 'att' parameter must be TITLE,KEY"),
        required=True,
    )

    form.widget(natura_2000_boolean_mapping=MultiSelect2FieldWidget)
    natura_2000_boolean_mapping = schema.List(
        title=_(u'Mapping of vocabularies values to boolean'),
        value_type=schema.Choice(
            title=_(u'Value'),
            vocabulary='urban.vocabulary.Natura2000',
        ),
        required=False,
    )

    natura_2000_boolean_mapping_value = schema.Choice(
        title=_(u'Boolean mapping value'),
        values=(True, False),
        required=True,
        default=True,
    )


class IReparcellingSettings(model.Schema):

    model.fieldset(
        'reparcelling',
        label=_('Reparcelling Vocabulary'),
        fields=[
            'reparcelling_url',
            'reparcelling_boolean_mapping',
            'reparcelling_boolean_mapping_value',
        ],
    )

    reparcelling_url = schema.TextLine(
        title=_(u'URL'),
        description=_(u"The order of the 'att' parameter must be TITLE,KEY"),
        required=True,
    )

    form.widget(reparcelling_boolean_mapping=MultiSelect2FieldWidget)
    reparcelling_boolean_mapping = schema.List(
        title=_(u'Mapping of vocabularies values to boolean'),
        value_type=schema.Choice(
            title=_(u'Value'),
            vocabulary='urban.vocabulary.Reparcelling',
        ),
        required=False,
    )

    reparcelling_boolean_mapping_value = schema.Choice(
        title=_(u'Boolean mapping value'),
        values=(True, False),
        required=True,
        default=True,
    )


class IParcellingsSettings(model.Schema):

    model.fieldset(
        'parcellings',
        label=_('Parcellings Vocabulary'),
        fields=[
            'parcellings_url',
            'parcellings_boolean_mapping',
            'parcellings_boolean_mapping_value',
        ],
    )

    parcellings_url = schema.TextLine(
        title=_(u'URL'),
        description=_(u"The order of the 'att' parameter must be TITLE,KEY"),
        required=True,
    )

    form.widget(parcellings_boolean_mapping=MultiSelect2FieldWidget)
    parcellings_boolean_mapping = schema.List(
        title=_(u'Mapping of vocabularies values to boolean'),
        value_type=schema.Choice(
            title=_(u'Value'),
            vocabulary='urban.vocabulary.Parcellings',
        ),
        required=False,
    )

    parcellings_boolean_mapping_value = schema.Choice(
        title=_(u'Boolean mapping value'),
        values=(True, False),
        required=True,
        default=True,
    )


class IProtectedBuildingSettings(model.Schema):

    model.fieldset(
        'protected_building',
        label=_('ProtectedBuilding Vocabulary'),
        fields=[
            'protected_building_url',
            'protected_building_boolean_mapping',
            'protected_building_boolean_mapping_value',
        ],
    )

    protected_building_url = schema.List(
        title=_(u'URL(s)'),
        description=_(u"The order of the 'att' parameter must be TITLE,KEY"),
        value_type=schema.TextLine(title=_(u'URL')),
        required=True,
    )

    form.widget(protected_building_boolean_mapping=MultiSelect2FieldWidget)
    protected_building_boolean_mapping = schema.List(
        title=_(u'Mapping of vocabularies values to boolean'),
        value_type=schema.Choice(
            title=_(u'Value'),
            vocabulary='urban.vocabulary.ProtectedBuilding',
        ),
        required=False,
    )

    protected_building_boolean_mapping_value = schema.Choice(
        title=_(u'Boolean mapping value'),
        values=(True, False),
        required=True,
        default=True,
    )


class INoteworthyTreesSettings(model.Schema):

    model.fieldset(
        'noteworthy_trees',
        label=_('NoteworthyTrees Vocabulary'),
        fields=[
            'noteworthy_trees_url',
            'noteworthy_trees_boolean_mapping',
            'noteworthy_trees_boolean_mapping_value',
        ],
    )

    noteworthy_trees_url = schema.List(
        title=_(u'URL(s)'),
        description=_(u"The order of the 'att' parameter must be TITLE,KEY"),
        value_type=schema.TextLine(title=_(u'URL')),
        required=True,
    )

    form.widget(noteworthy_trees_boolean_mapping=MultiSelect2FieldWidget)
    noteworthy_trees_boolean_mapping = schema.List(
        title=_(u'Mapping of vocabularies values to boolean'),
        value_type=schema.Choice(
            title=_(u'Value'),
            vocabulary='urban.vocabulary.NoteworthyTrees',
        ),
        required=False,
    )

    noteworthy_trees_boolean_mapping_value = schema.Choice(
        title=_(u'Boolean mapping value'),
        values=(True, False),
        required=True,
        default=True,
    )


class ITownPlanningEnvironmentReportsSettings(model.Schema):

    model.fieldset(
        'town_planning_environment_reports',
        label=_('TownPlanningEnvironmentReports Vocabulary'),
        fields=[
            'town_planning_environment_reports_url',
            'town_planning_environment_reports_boolean_mapping',
            'town_planning_environment_reports_boolean_mapping_value',
        ],
    )

    town_planning_environment_reports_url = schema.TextLine(
        title=_(u'URL'),
        description=_(u"The order of the 'att' parameter must be TITLE,KEY"),
        required=True,
    )

    form.widget(town_planning_environment_reports_boolean_mapping=MultiSelect2FieldWidget)
    town_planning_environment_reports_boolean_mapping = schema.List(
        title=_(u'Mapping of vocabularies values to boolean'),
        value_type=schema.Choice(
            title=_(u'Value'),
            vocabulary='urban.vocabulary.TownPlanningEnvironmentReports',
        ),
        required=False,
    )

    town_planning_environment_reports_boolean_mapping_value = schema.Choice(
        title=_(u'Boolean mapping value'),
        values=(True, False),
        required=True,
        default=True,
    )


class ISOLSettings(model.Schema):

    model.fieldset(
        'sol',
        label=_('SOL Vocabulary'),
        fields=[
            'sol_url',
            'sol_boolean_mapping',
            'sol_boolean_mapping_value',
        ],
    )

    sol_url = schema.TextLine(
        title=_(u'URL'),
        description=_(u"The order of the 'att' parameter must be TITLE,KEY"),
        required=True,
    )

    form.widget(sol_boolean_mapping=MultiSelect2FieldWidget)
    sol_boolean_mapping = schema.List(
        title=_(u'Mapping of vocabularies values to boolean'),
        value_type=schema.Choice(
            title=_(u'Value'),
            vocabulary='urban.vocabulary.SOLZones',
        ),
        required=False,
    )

    sol_boolean_mapping_value = schema.Choice(
        title=_(u'Boolean mapping value'),
        values=(True, False),
        required=True,
        default=True,
    )


class IUrbanRenovationSettings(model.Schema):

    model.fieldset(
        'urban_renovation',
        label=_('UrbanRenovation Vocabulary'),
        fields=[
            'urban_renovation_url',
            'urban_renovation_boolean_mapping',
            'urban_renovation_boolean_mapping_value',
        ],
    )

    urban_renovation_url = schema.TextLine(
        title=_(u'URL'),
        description=_(u"The order of the 'att' parameter must be TITLE,KEY"),
        required=True,
    )

    form.widget(urban_renovation_boolean_mapping=MultiSelect2FieldWidget)
    urban_renovation_boolean_mapping = schema.List(
        title=_(u'Mapping of vocabularies values to boolean'),
        value_type=schema.Choice(
            title=_(u'Value'),
            vocabulary='urban.vocabulary.UrbanRenovation',
        ),
        required=False,
    )

    urban_renovation_boolean_mapping_value = schema.Choice(
        title=_(u'Boolean mapping value'),
        values=(True, False),
        required=True,
        default=True,
    )


class IUrbanRevivalSettings(model.Schema):

    model.fieldset(
        'urban_revival',
        label=_('UrbanRevival Vocabulary'),
        fields=[
            'urban_revival_url',
            'urban_revival_boolean_mapping',
            'urban_revival_boolean_mapping_value',
        ],
    )

    urban_revival_url = schema.TextLine(
        title=_(u'URL'),
        description=_(u"The order of the 'att' parameter must be TITLE,KEY"),
        required=True,
    )

    form.widget(urban_revival_boolean_mapping=MultiSelect2FieldWidget)
    urban_revival_boolean_mapping = schema.List(
        title=_(u'Mapping of vocabularies values to boolean'),
        value_type=schema.Choice(
            title=_(u'Value'),
            vocabulary='urban.vocabulary.UrbanRevival',
        ),
        required=False,
    )

    urban_revival_boolean_mapping_value = schema.Choice(
        title=_(u'Boolean mapping value'),
        values=(True, False),
        required=True,
        default=True,
    )


class IAreaPlanSettings(model.Schema):

    model.fieldset(
        'area_plan',
        label=_('AreaPlan Vocabulary'),
        fields=[
            'area_plan_url',
            'area_plan_boolean_mapping',
            'area_plan_boolean_mapping_value',
        ],
    )

    area_plan_url = schema.List(
        title=_(u'URL(s)'),
        description=_(u"The order of the 'att' parameter must be TITLE,KEY"),
        value_type=schema.TextLine(title=_(u'URL')),
        required=True,
    )

    form.widget(area_plan_boolean_mapping=MultiSelect2FieldWidget)
    area_plan_boolean_mapping = schema.List(
        title=_(u'Mapping of vocabularies values to boolean'),
        value_type=schema.Choice(
            title=_(u'Value'),
            vocabulary='urban.vocabulary.AreaPlan',
        ),
        required=False,
    )

    area_plan_boolean_mapping_value = schema.Choice(
        title=_(u'Boolean mapping value'),
        values=(True, False),
        required=True,
        default=True,
    )


class ISARSettings(model.Schema):

    model.fieldset(
        'sar',
        label=_('SAR Vocabulary'),
        fields=[
            'sar_url',
            'sar_boolean_mapping',
            'sar_boolean_mapping_value',
        ],
    )

    sar_url = schema.TextLine(
        title=_(u'URL'),
        description=_(u"The order of the 'att' parameter must be TITLE,KEY"),
        required=True,
    )

    form.widget(sar_boolean_mapping=MultiSelect2FieldWidget)
    sar_boolean_mapping = schema.List(
        title=_(u'Mapping of vocabularies values to boolean'),
        value_type=schema.Choice(
            title=_(u'Value'),
            vocabulary='urban.vocabulary.SAR',
        ),
        required=False,
    )

    sar_boolean_mapping_value = schema.Choice(
        title=_(u'Boolean mapping value'),
        values=(True, False),
        required=True,
        default=True,
    )


class IKarsticSettings(model.Schema):

    model.fieldset(
        'karstic',
        label=_('Karstic Vocabulary'),
        fields=[
            'karstic_url',
            'karstic_boolean_mapping',
            'karstic_boolean_mapping_value',
        ],
    )

    karstic_url = schema.TextLine(
        title=_(u'URL'),
        description=_(u"The order of the 'att' parameter must be TITLE,KEY"),
        required=True,
    )

    form.widget(karstic_boolean_mapping=MultiSelect2FieldWidget)
    karstic_boolean_mapping = schema.List(
        title=_(u'Mapping of vocabularies values to boolean'),
        value_type=schema.Choice(
            title=_(u'Value'),
            vocabulary='urban.vocabulary.Karstic',
        ),
        required=False,
    )

    karstic_boolean_mapping_value = schema.Choice(
        title=_(u'Boolean mapping value'),
        values=(True, False),
        required=True,
        default=True,
    )


class ICatchmentAreaSettings(model.Schema):

    model.fieldset(
        'catchment_area',
        label=_('CatchmentArea Vocabulary'),
        fields=[
            'catchment_area_url',
            'catchment_area_boolean_mapping',
            'catchment_area_boolean_mapping_value',
        ],
    )

    catchment_area_url = schema.List(
        title=_(u'URL(s)'),
        description=_(u"The order of the 'att' parameter must be TITLE,KEY"),
        value_type=schema.TextLine(title=_(u'URL')),
        required=True,
    )

    form.widget(catchment_area_boolean_mapping=MultiSelect2FieldWidget)
    catchment_area_boolean_mapping = schema.List(
        title=_(u'Mapping of vocabularies values to boolean'),
        value_type=schema.Choice(
            title=_(u'Value'),
            vocabulary='urban.vocabulary.CatchmentArea',
        ),
        required=False,
    )

    catchment_area_boolean_mapping_value = schema.Choice(
        title=_(u'Boolean mapping value'),
        values=(True, False),
        required=True,
        default=True,
    )


class ISettings(IPCASettings,
                INatura2000Settings,
                IReparcellingSettings,
                IParcellingsSettings,
                IProtectedBuildingSettings,
                INoteworthyTreesSettings,
                ITownPlanningEnvironmentReportsSettings,
                ISOLSettings,
                IUrbanRenovationSettings,
                IUrbanRevivalSettings,
                IAreaPlanSettings,
                ISARSettings,
                IKarsticSettings,
                ICatchmentAreaSettings):
    """ """

    enable = schema.Bool(
        title=_(u'Enable Coring service'),
        required=True,
    )

    base_query = schema.TextLine(
        title=_(u'Coring service base query'),
        required=True,
    )


class IVocabularies(Interface):

    pca_cached = schema.List(
        title=_(u'PCA cached value'),
        value_type=schema.List(
            title=u'Vocabulary record',
            value_type=schema.TextLine(title=u'Value'),
            required=False,
        ),
        required=False,
    )

    natura_2000_cached = schema.List(
        title=_(u'Natura 2000 cached value'),
        value_type=schema.List(
            title=u'Vocabulary record',
            value_type=schema.TextLine(title=u'Value'),
            required=False,
        ),
        required=False,
    )

    reparcelling_cached = schema.List(
        title=_(u'Reparcelling cached value'),
        value_type=schema.List(
            title=u'Vocabulary record',
            value_type=schema.TextLine(title=u'Value'),
            required=False,
        ),
        required=False,
    )

    parcellings_cached = schema.List(
        title=_(u'Parcellings cached value'),
        value_type=schema.List(
            title=u'Vocabulary record',
            value_type=schema.TextLine(title=u'Value'),
            required=False,
        ),
        required=False,
    )

    protected_building_cached = schema.List(
        title=_(u'ProtectedBuilding cached value'),
        value_type=schema.List(
            title=u'Vocabulary record',
            value_type=schema.TextLine(title=u'Value'),
            required=False,
        ),
        required=False,
    )

    noteworthy_trees_cached = schema.List(
        title=_(u'PCA cached value'),
        value_type=schema.List(
            title=u'Vocabulary record',
            value_type=schema.TextLine(title=u'Value'),
            required=False,
        ),
        required=False,
    )

    town_planning_environment_reports_cached = schema.List(
        title=_(u'TownPlanningEnvironmentReports cached value'),
        value_type=schema.List(
            title=u'Vocabulary record',
            value_type=schema.TextLine(title=u'Value'),
            required=False,
        ),
        required=False,
    )

    sol_cached = schema.List(
        title=_(u'SOL cached value'),
        value_type=schema.List(
            title=u'Vocabulary record',
            value_type=schema.TextLine(title=u'Value'),
            required=False,
        ),
        required=False,
    )

    urban_renovation_cached = schema.List(
        title=_(u'UrbanRenovation cached value'),
        value_type=schema.List(
            title=u'Vocabulary record',
            value_type=schema.TextLine(title=u'Value'),
            required=False,
        ),
        required=False,
    )

    urban_revival_cached = schema.List(
        title=_(u'UrbanRevival cached value'),
        value_type=schema.List(
            title=u'Vocabulary record',
            value_type=schema.TextLine(title=u'Value'),
            required=False,
        ),
        required=False,
    )

    area_plan_cached = schema.List(
        title=_(u'AreaPlan cached value'),
        value_type=schema.List(
            title=u'Vocabulary record',
            value_type=schema.TextLine(title=u'Value'),
            required=False,
        ),
        required=False,
    )

    sar_cached = schema.List(
        title=_(u'SAR cached value'),
        value_type=schema.List(
            title=u'Vocabulary record',
            value_type=schema.TextLine(title=u'Value'),
            required=False,
        ),
        required=False,
    )

    karstic_cached = schema.List(
        title=_(u'Karstic cached value'),
        value_type=schema.List(
            title=u'Vocabulary record',
            value_type=schema.TextLine(title=u'Value'),
            required=False,
        ),
        required=False,
    )

    catchment_area_cached = schema.List(
        title=_(u'CatchmentArea cached value'),
        value_type=schema.List(
            title=u'Vocabulary record',
            value_type=schema.TextLine(title=u'Value'),
            required=False,
        ),
        required=False,
    )
