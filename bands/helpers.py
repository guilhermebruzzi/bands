#-*- coding:utf-8 -*-

import unicodedata
import re

def get_slug(title):
    slug = unicodedata.normalize('NFKD', unicode(title))
    slug = slug.encode('ascii', 'ignore').lower()
    slug = re.sub(r'[^a-z0-9]+', '-', slug).strip('-')
    slug = re.sub(r'[-]+', '-', slug)
    return slug

#def get_project(slug_project):
#    project = Project.objects.get_or_404(slug=slug_project)
#    project.supporters.append(project.owner) # Inclui automaticamente o Dono do projeto como supporter dele
#    return {
#        "title": project.title,
#        "description": project.description,
#        "link": project.link,
#        "supporters": [{"name": supporter.name, "photo": supporter.photo} for supporter in project.supporters]
#    }
#    
#def create_project(**data):
#    project = Project()
#    project.title = data["title"]
#    project.slug = get_slug(data["title"])
#    project.description = data["description"]
#    project.link = data["link"]
#    project.owner = data["owner"]
#    project.save()
#    return project
#
#def get_or_create_supporter(data):
#    (supporter, created) = Supporter.objects.get_or_create(facebook_id=data['id'], email=data['email'], name=data['name'])
#    return supporter
