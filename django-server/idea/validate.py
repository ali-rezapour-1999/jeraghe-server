from base.validate import validate_required_field


def validate_idea(data):
    validate_required_field(data.get("title"), "عنوان")
    validate_required_field(data.get("category"), "دسته بندی")
    validate_required_field(data.get("status"), "وضعیت")
    if str(data.get("needs_collaborators")).lower() == "true":
        validate_required_field(data.get("required_skills"), "نیازمندی‌ها")
        validate_required_field(data.get("collaboration_type"), "نوع همکاری")

    return data
