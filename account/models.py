from django.db import models

class User(models.Model):
    """Usernames for platform users.

    Authentication is to be done through LDAP or other plugins.
    """

    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    last_accessed = models.DateTimeField(blank=True, null=True)

class Committee(models.Model):
    """Generic committee model.

    Sub-committees will have to be added as separate models and referred to as such.
    """

    name = models.CharField(max_length=30, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    description = models.TextField()

    def __str__(self):
        return self.name + '—' + self.description[:20] + '...'

class Role(models.Model):
    """Role and the associated committee relation."""


    name = models.CharField(max_length=30, default='Member')
    committee = models.ForeignKey(Committee, related_name='com_roles', on_delete=models.CASCADE)
    description = models.TextField(default="Describe this role's functionality.")

    def __str__(self):
        return self.name + ' of ' + self.committee.name + ' (' + self.description[:20] + '...)'

    class Meta:
        unique_together = ('committee', 'name')

class Member(models.Model):
    """Members of committees with associated roles."""
    user = models.ForeignKey(User, related_name='membership', on_delete=models.CASCADE)
    role = models.ForeignKey(Role, related_name='member', on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + ' ' + self.role.name

    class Meta:
        unique_together = ('user', 'role')

