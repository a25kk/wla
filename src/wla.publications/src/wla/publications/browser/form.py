# -*- coding: utf-8 -*-

from __future__ import print_function
from smtplib import SMTPException, SMTPRecipientsRefused

import z3c.form
from plone.app.uuid.utils import uuidToObject
from plone.autoform import directives
from plone.autoform.form import AutoExtensibleForm
from plone.registry.interfaces import IRegistry
from plone.supermodel import model
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces.controlpanel import IMailSchema
from Products.statusmessages.interfaces import IStatusMessage
from z3c.form import button, form
from zope import schema
from zope.browserpage.viewpagetemplatefile import \
    ViewPageTemplateFile as Zope3PageTemplateFile
from zope.component import getMultiAdapter, getUtility
from zope.interface import Invalid, invariant
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from wla.publications import _
from wla.publications.utils import trusted, validateaddress

greetings = SimpleVocabulary(
    [
     SimpleTerm(value='--NOVALUE--', title=_(u'select value')),
     SimpleTerm(value='An', title=_(u'An')),
     SimpleTerm(value='Ehepaar', title=_(u'Ehepaar')),
     SimpleTerm(value='Familie', title=_(u'Familie')),
     SimpleTerm(value='Firma', title=_(u'Firma')),
     SimpleTerm(value='Frau', title=_(u'Frau')),
     SimpleTerm(value='Herr', title=_(u'Herr')),
     SimpleTerm(value='Herr und Frau', title=_(u'Herr und Frau')),

     ]
    )

titles = SimpleVocabulary(
    [SimpleTerm(value='--NOVALUE--', title=_(u'select value')),
     SimpleTerm(value='Dr.', title=_(u'Dr.')),
     SimpleTerm(value='Professor', title=_(u'Professor')),
     SimpleTerm(value='Prof. Dr.', title=_(u'Prof. Dr.'))

     ]
    )

class IOrderForm(model.Schema):
    """ Define form fields """
    greeting = schema.List(title = _(u'greeting'), required = True, value_type=schema.Choice(source=greetings))
    titles = schema.List(title = _(u'title'), required = True, value_type=schema.Choice(source=titles))

    organization = schema.TextLine(title=_(u'Organization'), required=False)

    lastname = schema.TextLine(title=_(u'Lastname'), required=True)
    firstname = schema.TextLine(title=_(u'Firstname'), required=True)

    street = schema.TextLine(title=_(u'Street'), required=True)
    number = schema.TextLine(title=_(u'Number'), required=True)
    zipcode = schema.TextLine(title=_(u'Zipcode'), required=True)
    city = schema.TextLine(title=_(u'City'), required=True)
    country = schema.TextLine(title=_(u'Country'), required=True)

    email = schema.TextLine(title=_(u'Email'), required=True, constraint=validateaddress)
    phone = schema.TextLine(title=_(u'Phone'), required=False)

    publications = schema.Text(
            title=_(u"publications")
        )
    directives.widget(greeting=z3c.form.browser.select.SelectFieldWidget)
    directives.widget(titles=z3c.form.browser.select.SelectFieldWidget)

class OrderForm(AutoExtensibleForm, form.Form):
    """ Define Form handling

    This form can be accessed as http://yoursite/@@greeting-form

    """
    template = Zope3PageTemplateFile("form.pt")
    schema = IOrderForm
    ignoreContext = True

    def getTitles(self, value):
        for i in titles:
            if i.value in value:
                return self.context.translate(i.title)


    def getGreeting(self, value):
        for i in greetings:
            if i.value in value:
                return self.context.translate(i.title)

    def getList(self):
        context = self.context
        path = context.getPhysicalPath()
        items = context.portal_catalog(path={'query': "/".join(path), 'depth': 1},portal_type = 'publication', sort_on='getObjPositionInParent')
        return items

    def _redirect(self, target=''):
        if not target:
            portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
            target = portal_state.portal_url()
        self.request.response.redirect(target)


    @z3c.form.button.buttonAndHandler(_(u'Send'))
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        portal = getToolByName(self, 'portal_url').getPortalObject()
        encoding = portal.getProperty('email_charset', 'utf-8')

        result = data['publications'].split(",")

        publications = []

        for p in result:
            k = p.split(":")
            if len(k) == 2:
                image = uuidToObject(k[0])
                qty = k[1]
                publications.append([image, qty])


        data['publications'] = publications
        data['greeting'] = self.getGreeting(data['greeting'])
        data['titles'] = self.getTitles(data['titles'])
        trusted_template = trusted(portal.order_email)

        mail_text = trusted_template(self, charset=encoding, data = data)

        subject = self.context.translate(_(u"New order"))

        if isinstance(mail_text, str):
            mail_text = mail_text.encode(encoding)

        host = getToolByName(self, 'MailHost')

        registry = getUtility(IRegistry)
        mail_settings = registry.forInterface(IMailSchema, prefix='plone')
        m_to = mail_settings.email_from_address

        # to admin

        m_from = m_to


        try:
            host.send(mail_text, m_to, m_from, subject=subject,
                      charset=encoding, immediate=True, msg_type="text/html")

            print(m_to)

        except SMTPRecipientsRefused:

            raise SMTPRecipientsRefused(
                _(u'Recipient address rejected by server.'))

        except SMTPException as e:
            raise(e)

        # to client

        trusted_template = trusted(portal.order_email2)

        mail_text = trusted_template(self, charset=encoding, data = data)

        subject = self.context.translate(_(u"New order"))

        if isinstance(mail_text, str):
            mail_text = mail_text.encode(encoding)


        try:
            host.send(mail_text, data['email'], m_from, subject=subject,
                      charset=encoding, immediate=True, msg_type="text/html")


        except SMTPRecipientsRefused:

            raise SMTPRecipientsRefused(
                _(u'Recipient address rejected by server.'))

        except SMTPException as e:
            raise(e)


        IStatusMessage(self.request).add(_(u"Submit complete"), type='info')
        return self._redirect(target=self.context.absolute_url())


    @z3c.form.button.buttonAndHandler(_(u"Cancel"))
    def handleCancel(self, action):
        """User cancelled. Redirect back to the front page.
        """
