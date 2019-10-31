from datetime import timedelta
import logging
from typing import Optional, List, Dict

from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
import django_rq

from autoemails.models import Trigger, Template
from workshops.models import Event, Role
from workshops.util import match_notification_email, human_daterange


logger = logging.getLogger('amy.signals')
scheduler = django_rq.get_scheduler('default')


class Action:
    """
    Base class interface for actions triggered by our predefined triggers.
    This class can handle condition checking for whether the action should
    launch, but most importantly acts as a refresher for DB data.  It was
    intended to support lazy binding / refreshing DB data before actual email
    is built and sent out.
    """

    # Keeps the default timestamp for the job to run
    launch_at: Optional[timedelta] = None
    # Stores additional contextual data for the trigger/template
    additional_context: Optional[Dict] = None

    def __init__(self, trigger: Trigger, objects: Optional[Dict] = None):
        # save parameters just in case
        self.trigger = trigger
        self.template = trigger.template
        self.context_objects = objects

        # default values for fields that will become values later on
        self.context = None
        self.email = None

    @staticmethod
    def check(cls, *args, **kwargs):
        """This static method can be used to determine if conditions are met
        for creating an Action instance."""
        raise NotImplementedError()

    def get_launch_at(self, *args, **kwargs):
        return self.launch_at

    def get_additional_context(self, *args, **kwargs):
        return self.additional_context

    def _context(self, additional_context: Optional[Dict] = None) -> Dict:
        """Prepare general context for lazy-evaluated email message used later
        on."""
        context = dict(site=Site.objects.get_current())
        if additional_context:
            context.update(additional_context)
        return context

    def _email(self, *args, **kwargs) -> EmailMultiAlternatives:
        # gather context (it should refresh all related objects from DB)
        adt_context = self.get_additional_context(objects=self.context_objects)
        self.context = self._context(adt_context)

        # refresh trigger/template DB information
        self.trigger.refresh_from_db()
        self.template = self.trigger.template

        # build email
        email = self.template.build_email(context)
        return email

    def __call__(self, *args, **kwargs):
        # gather context and build email
        self.email = self._email()

        # send email
        return self.email.send(fail_silently=False)


class NewInstructorAction(Action):
    """
    Action for informing instructors about workshop they've been accepted to.

    How to use it:

    >>> triggers = Trigger.objects.filter(active=True, action='new-instructor')
    >>> for trigger in triggers:
    ...     action = NewInstructorAction(
    ...         trigger=trigger,
    ...         objects=dict(event=event, task=task),
    ...     )
    ...     launch_at = action.get_launch_at()
    ...     job = scheduler.enqueue_in(launch_at, action)
    """

    # it should be at least 1 hour to give admin some time in case of mistakes
    launch_at = timedelta(hours=1)

    @staticmethod
    def check(event: Event, role: Role):
        """Conditions for creating a NewInstructorAction."""
        return (
            role.name == 'instructor' and
            event in Event.objects.upcoming_events()
        )

    def get_additional_context(self, objects, *args, **kwargs):
        # refresh related event
        event = objects['event']
        task = objects['task']
        event.refresh_from_db()
        task.refresh_from_db()

        # prepare context
        context['workshop'] = event
        context['workshop_main_type'] = None
        tmp = event.tags.carpentries().first()
        if tmp:
            context['workshop_main_type'] = tmp.name
        context['dates'] = None
        if event.start and event.end:
            context['dates'] = human_daterange(event.start, event.end)
        context['host'] = event.host
        context['regional_coordinator_email'] = \
            list(match_notification_email(event))
        context['person'] = task.person
        context['instructor'] = task.person
        context['role'] = task.role
        context['assignee'] = (
            event.assigned_to.full_name
            if event.assigned_to
            else 'Regional Coordinator'
        )

        return context