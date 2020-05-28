# -*- coding: utf-8 -*-
from gene.tumour import _

from plone import api
from zope.i18n import translate
from zope.interface import implementer, provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from Products.CMFPlone.utils import safe_unicode

situation_dict = {
    u'surgery': _(u'Surgery'),
    u'chemotherapy': _(u'Chemotherapy'),
    u'radiotherapy': _(u'Radiotherapy'),
    u'targeted-therapy': _(u'Targeted drug therapy'),
}
invert_situation_dict = {val: key for key, val in situation_dict.items()}


@provider(IVocabularyFactory)
def treatment_situation(context):
    treatment_vocabulary = SimpleVocabulary(
        [SimpleTerm(value=value, title=title)
         for value, title in situation_dict.items()]
    )
    return treatment_vocabulary


na_types_dict = {
    u'cfDNA': _(u'cfDNA'),
    u'gDNA': _(u'gDNA'),
    u'RNA': _(u'RNA'),
    u'gDNA\RNA': _(u'gDNA\RNA'),
    u'cfDNA\RNA': _(u'cfDNA\RNA'),
}
invert_na_types_dict = {val: key for key, val in na_types_dict.items()}


@implementer(IVocabularyFactory)
class NATypes(object):

    def __call__(self, context):
        na_vocabulary = SimpleVocabulary(
            [SimpleTerm(value=value, title=title)
             for value, title in na_types_dict.items()]
        )
        return na_vocabulary


result_dict = {
    u'negative': _(u'Negative'),
    u'positive': _(u'Positive'),
}
invert_result_dict = {val: key for key, val in result_dict.items()}


@provider(IVocabularyFactory)
def analysis_result(context):
    result_vocabulary = SimpleVocabulary(
        [SimpleTerm(value=value, title=title)
         for value, title in result_dict.items()]
    )
    return result_vocabulary


@provider(IVocabularyFactory)
def progress_steps(context):
    steps_vocabulary = SimpleVocabulary(
        [SimpleTerm(value=u'step1', title=_(u'Blood Sample')),
         SimpleTerm(value=u'step2', title=_(u'NA Extraction')),
         SimpleTerm(value=u'step3', title=_(u'Library Construction')),
         SimpleTerm(value=u'step4', title=_(u'Computer Detecting')),
         SimpleTerm(value=u'step5', title=_(u'Analysis Results'))]
    )
    return steps_vocabulary


@implementer(IVocabularyFactory)
class RedoSteps(object):

    def __call__(self, context):
        steps_vocabulary = SimpleVocabulary(
            [SimpleTerm(value=u'step2', title=_(u'NA Extraction')),
             SimpleTerm(value=u'step3', title=_(u'Library Construction')),
             SimpleTerm(value=u'step4', title=_(u'Computer Detecting'))]
        )
        return steps_vocabulary


@implementer(IVocabularyFactory)
class ReviewStates(object):

    def __call__(self, context):
        if isinstance(context, dict) and 'uuid' in context:
            obj = api.content.uuidToObject(context['uuid'])
            workflow = api.portal.get_tool('portal_workflow')
            actions = workflow.listActions(object=obj)

            states_vocabulary = SimpleVocabulary(
                [SimpleTerm(value=action['id'],
                            title=translate(_(action['name']),
                                            context=api.portal.getRequest()))
                 for action in actions]
            )
        else:
            states_vocabulary = SimpleVocabulary([])
        return states_vocabulary


_(u'step1')
_(u'step2')
_(u'step3')
_(u'step4')
_(u'step5')

@implementer(IVocabularyFactory)
class DetectionPlan(object):

    def __call__(self,context):
        
        plans = api.portal.get_registry_record(
            'gene.tumour.interfaces.IGeneTumourSettings.'
            'detection_plan') 
       
        if plans is None:
            return SimpleVocabulary([])
        
        def safe_encode(term):
            if isinstance(term, unicode):
                # no need to use portal encoding for transitional encoding from
                # unicode to ascii. utf-8 should be fine.
                term = term.encode('utf-8')
            return term

        # Vocabulary term tokens *must* be 7 bit values, titles *must* be
        # unicode
        newplans = map(safe_encode,plans)
        def split_code(item):
            if "-" not in item: return  item
            ars = item.split("-")
            num = len(ars)
            if num > 2:
                rs = []
                for j in range(num -1):
                    rs .append(ars[j]) 
                return u"-".join(rs)
            else:
                return ars[0]

        items = [
            SimpleTerm(value=safe_unicode(i),token=split_code(i),title= safe_unicode(i))
            for i in newplans
        ]
        return SimpleVocabulary(items)