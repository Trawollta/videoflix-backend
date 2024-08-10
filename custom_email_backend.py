import ssl
import certifi
from django.core.mail.backends.smtp import EmailBackend

class CustomEmailBackend(EmailBackend):
    def _get_ssl_context(self):
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        ssl_context.check_hostname = True
        ssl_context.verify_mode = ssl.CERT_REQUIRED
        return ssl_context

    def open(self):
        if self.connection:
            return False
        connection_params = self.get_connection_params()
        if connection_params.get('use_ssl'):
            self.connection = self.connection_class(context=self._get_ssl_context(), **connection_params)
        else:
            self.connection = self.connection_class(**connection_params)
            if self.use_tls:
                self.connection.starttls(context=self._get_ssl_context())
        self.connection.set_debuglevel(self.debug_level)
        self.connection.login(self.username, self.password)
        return True
