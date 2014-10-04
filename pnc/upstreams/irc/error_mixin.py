from traceback import format_exception

from twisted.python import log


class PNCErrorMixin:
    """Handle certain misformatted messages.

    We put these into their own class for organization purposes.
    """
    def badMessage(self, line, excType, excValue, tb):
        """Called when I get a message that's so broken I can't use it.
        """
        log.msg('Broken message: %s' % line)
        log.msg(format_exception(excType, excValue, tb))

    def quirkyMessage(self, message):
        """This is called when I receive a message which is peculiar
        """
        log.msg('Quirky message: %s' % message)
