from django.contrib import admin

# Register your models here.
from .models import ( Content,
                     Illustration, 
                 
                    PreviousState, 
                    CurrentActiveState,
                    CompletedState,
                    CurrentActiveNode,
                    PreviousActiveNode

                    )
admin.site.register(Content)
admin.site.register(Illustration)

admin.site.register(PreviousState)
admin.site.register(CurrentActiveState)
admin.site.register(CompletedState)
admin.site.register(CurrentActiveNode)
admin.site.register(PreviousActiveNode)