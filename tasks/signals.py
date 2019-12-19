from django.db.models.signals import m2m_changed, post_save, post_delete
from django.dispatch import receiver
from tasks.models import TodoItem, Category, Priority, PriorityCount, CategoryCount
from django.contrib.auth.models import User
from collections import Counter


@receiver(post_save, sender=TodoItem)
def task_changed(sender, instance, created, **kwargs):
    pr_counter = Counter()

    for pr in PriorityCount.objects.all():
        pr_counter[pr.priority] = 0

    for t in TodoItem.objects.filter(owner=instance.owner):
        pr_counter[t.priority] +=1
    
    for pr, new_count in pr_counter.items():
        pc_qs = PriorityCount.objects.filter(priority=pr).filter(owner=instance.owner)
        if pc_qs.count():
            pc_qs.update(priority_count=new_count)
        else:
            PriorityCount.objects.create(priority=pr, owner=instance.owner, priority_count=new_count)

@receiver(post_delete, sender=TodoItem)
def task_deleted(sender, instance, **kwargs):
    p_count = TodoItem.objects.filter(owner=instance.owner).filter(priority=instance.priority).count()
    if PriorityCount.objects.filter(priority=instance.priority).filter(owner=instance.owner):
        PriorityCount.objects.filter(owner=instance.owner).filter(priority=instance.priority).update(priority_count=p_count)
    else:
        PriorityCount.objects.create(priority=instance.priority, owner=instance.owner, priority_count=p_count)

    cat_counter = Counter()
    
    for cc in CategoryCount.objects.filter(owner=instance.owner):
        cat = cc.category
        cat_counter[cat.id] = 0

    for t in TodoItem.objects.filter(owner=instance.owner):
        for cat in t.category.all():
            cat_counter[cat.id] += 1

    for id, new_count in cat_counter.items():
        cat = Category.objects.filter(id=id).first()
        CategoryCount.objects.filter(owner=instance.owner).filter(category=cat).update(category_count=new_count)


@receiver(m2m_changed, sender=TodoItem.category.through)
def task_cats_added(sender, instance, action, model, **kwargs):
    if action != "post_add":
        return

    for cat in instance.category.all():
        slug = cat.slug

        new_count = 0
        for task in TodoItem.objects.filter(owner=instance.owner):
            new_count += task.category.filter(slug=slug).count()
        
        cat_qs = CategoryCount.objects.filter(owner=instance.owner).filter(category=cat)
        if cat_qs.count() > 0:
            cat_qs.update(category_count=new_count)
        else:
            CategoryCount.objects.create(category=cat, owner=instance.owner, category_count=new_count)


@receiver(m2m_changed, sender=TodoItem.category.through)
def task_cats_removed(sender, instance, action, model, pk_set, **kwargs):
    if action != "post_remove":
        return

    cat_counter = Counter()

    for cc in CategoryCount.objects.filter(owner=instance.owner):
        cat = cc.category
        cat_counter[cat.id] = 0

    for t in TodoItem.objects.filter(owner=instance.owner):
        for cat in t.category.all():
            cat_counter[cat.id] += 1

    for id, new_count in cat_counter.items():
        cat = Category.objects.filter(id=id).first()
        if cat:
            cat_qs = CategoryCount.objects.filter(owner=instance.owner).filter(category=cat)
            if cat_qs.count():
                cat_qs.update(category_count=new_count)
            else:
                CategoryCount.objects.create(category=cat, owner=instance.owner, category_count=new_count)
