from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Student, Class

def update_class_student_count(class_obj):
    """更新班级的学生人数"""
    if class_obj:
        class_obj.student_count = Student.objects.filter(class_id=class_obj).count()
        class_obj.save(update_fields=['student_count'])

@receiver(post_save, sender=Student)
def student_post_save(sender, instance, created, **kwargs):
    """学生保存后更新班级学生人数"""
    # 如果是更新学生信息且班级发生变化
    if not created and hasattr(instance, '_original_class_id'):
        old_class = instance._original_class_id
        if old_class and old_class != instance.class_id:
            # 更新旧班级的学生人数
            update_class_student_count(old_class)
    
    # 更新新班级的学生人数
    update_class_student_count(instance.class_id)

@receiver(post_delete, sender=Student)
def student_post_delete(sender, instance, **kwargs):
    """学生删除后更新班级学生人数"""
    update_class_student_count(instance.class_id) 