#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Конструктор резюме - генерирует статические HTML и Markdown файлы из JSON конфигурации
"""

import json
import os
from datetime import datetime
from pathlib import Path


class ResumeBuilder:
    def __init__(self, data_file="resume_data.json"):
        """Инициализация конструктора резюме"""
        self.data_file = data_file
        self.data = self.load_data()

    def load_data(self):
        """Загрузка данных из JSON файла"""
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ Файл {self.data_file} не найден!")
            return {}
        except json.JSONDecodeError as e:
            print(f"❌ Ошибка в JSON файле: {e}")
            return {}

    def generate_markdown(self):
        """Генерация Markdown версии резюме"""
        md_content = []

        # Заголовок и контактная информация
        personal = self.data.get("personal_info", {})
        md_content.append("---")
        md_content.append("layout: default")
        md_content.append("---")
        md_content.append("")
        md_content.append(f"# {personal.get('name', 'Имя не указано')}")
        md_content.append("")

        if personal.get("email"):
            md_content.append(
                f"📧 Email: [{personal['email']}](mailto:{personal['email']})"
            )
        if personal.get("telegram"):
            md_content.append(
                f"💬 Telegram: [{personal['telegram']}](https://t.me/{personal['telegram'].replace('@', '')})"
            )
        if personal.get("github"):
            md_content.append(
                f"💻 GitHub: [{personal['github']}](https://{personal['github']})"
            )
        if personal.get("location"):
            md_content.append(f"📍 {personal['location']}")

        md_content.append("")
        md_content.append("---")
        md_content.append("")

        # Навыки
        skills = self.data.get("skills", {})
        if skills:
            md_content.append("## 🔧 Ключевые навыки")
            md_content.append("")

            if skills.get("languages"):
                md_content.append(f"**Языки:** {', '.join(skills['languages'])}")
            if skills.get("libraries"):
                md_content.append(f"**Библиотеки:** {', '.join(skills['libraries'])}")
            if skills.get("tools"):
                md_content.append(f"**Инструменты:** {', '.join(skills['tools'])}")

            md_content.append("")
            md_content.append("---")
            md_content.append("")

        # Опыт и проекты
        experience = self.data.get("experience", [])
        if experience:
            md_content.append("## 💼 Опыт / Проекты")
            md_content.append("")

            # Группировка по типам
            projects_by_type = {}
            for project in experience:
                project_type = project.get("type", "Проект")
                if project_type not in projects_by_type:
                    projects_by_type[project_type] = []
                projects_by_type[project_type].append(project)

            # Отображение групп проектов
            for project_type, projects in projects_by_type.items():
                if len(projects) > 1 or project_type != "Проект":
                    md_content.append(f"**{project_type}**")
                    md_content.append("")

                for project in projects:
                    # Название проекта как ссылка или простой текст
                    title = project.get("title", "Без названия")
                    if project.get("link"):
                        md_content.append(f"- **[{title}]({project['link']})**")
                    else:
                        md_content.append(f"- **{title}**")

                    if project.get("description"):
                        md_content.append(f"  Описание: {project['description']}")
                    if project.get("tech_stack"):
                        md_content.append(f"  Стек: {', '.join(project['tech_stack'])}")
                    if project.get("date"):
                        md_content.append(f"  *({project['date']})*")
                    md_content.append("")

            md_content.append("---")
            md_content.append("")

        # Образование
        education = self.data.get("education", {})
        if education:
            md_content.append("## 🎓 Образование")

            if isinstance(education, list):
                for edu in education:
                    if edu.get("institution"):
                        md_content.append(f"**{edu['institution']}**")
                    if edu.get("field"):
                        md_content.append(f"Направление: {edu['field']}")
                    if edu.get("degree"):
                        md_content.append(f"Степень: {edu['degree']}")
                    if edu.get("period"):
                        md_content.append(f"{edu['period']}")
                    md_content.append("")
            else:
                # Обратная совместимость
                if education.get("institution"):
                    md_content.append(f"**{education['institution']}**")
                if education.get("field"):
                    md_content.append(f"Направление: {education['field']}")
                if education.get("period"):
                    md_content.append(f"{education['period']}")

            md_content.append("")
            md_content.append("---")
            md_content.append("")

        # Сертификаты
        certificates = self.data.get("certificates", [])
        if certificates:
            md_content.append("## 📜 Сертификаты и курсы")
            for cert in certificates:
                md_content.append(f"- **{cert}**")
            md_content.append("")

        return "\n".join(md_content)

    def generate_html(self):
        """Генерация standalone HTML версии резюме"""
        personal = self.data.get("personal_info", {})

        html_content = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{personal.get('name', 'Резюме')}</title>
    <link rel="icon" type="image/x-icon" href="favicon.ico">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
            background-color: #fdfdfd;
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
            margin-bottom: 30px;
        }}
        h2 {{
            color: #34495e;
            margin-top: 40px;
            margin-bottom: 20px;
        }}
        .contact-info {{
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
        }}
        .contact-info p {{
            margin: 5px 0;
        }}
        .skills {{
            display: grid;
            gap: 15px;
            margin-bottom: 30px;
        }}
        .skill-category {{
            background-color: #f1f2f6;
            padding: 15px;
            border-radius: 6px;
        }}
        .skill-category strong {{
            color: #2f3542;
        }}
        .project {{
            background-color: #ffffff;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .project h3 {{
            margin-top: 0;
            color: #2c3e50;
        }}
        .project h3 a {{
            color: #2c3e50;
            text-decoration: none;
        }}
        .project h3 a:hover {{
            color: #3498db;
            text-decoration: underline;
        }}
        .tech-stack {{
            background-color: #e8f4f8;
            padding: 8px 12px;
            border-radius: 4px;
            font-size: 0.9em;
            margin-top: 10px;
        }}
        .date {{
            color: #7f8c8d;
            font-style: italic;
            font-size: 0.9em;
        }}
        a {{
            color: #3498db;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        .section {{
            margin-bottom: 40px;
        }}
        .emoji {{
            margin-right: 8px;
        }}
        ul {{
            padding-left: 20px;
        }}
        li {{
            margin-bottom: 10px;
        }}
        .generated-info {{
            text-align: center;
            color: #95a5a6;
            font-size: 0.8em;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ecf0f1;
        }}
    </style>
</head>
<body>
    <h1>{personal.get('name', 'Имя не указано')}</h1>
    
    <div class="contact-info">"""

        if personal.get("email"):
            html_content += f'\n        <p><span class="emoji">📧</span>Email: <a href="mailto:{personal["email"]}">{personal["email"]}</a></p>'
        if personal.get("telegram"):
            tg_handle = personal["telegram"].replace("@", "")
            html_content += f'\n        <p><span class="emoji">💬</span>Telegram: <a href="https://t.me/{tg_handle}">{personal["telegram"]}</a></p>'
        if personal.get("github"):
            html_content += f'\n        <p><span class="emoji">💻</span>GitHub: <a href="https://{personal["github"]}">{personal["github"]}</a></p>'
        if personal.get("location"):
            html_content += (
                f'\n        <p><span class="emoji">📍</span>{personal["location"]}</p>'
            )

        html_content += "\n    </div>"

        # Навыки
        skills = self.data.get("skills", {})
        if skills:
            html_content += '\n\n    <div class="section">\n        <h2><span class="emoji">🔧</span>Ключевые навыки</h2>\n        <div class="skills">'

            if skills.get("languages"):
                html_content += f'\n            <div class="skill-category"><strong>Языки:</strong> {", ".join(skills["languages"])}</div>'
            if skills.get("libraries"):
                html_content += f'\n            <div class="skill-category"><strong>Библиотеки:</strong> {", ".join(skills["libraries"])}</div>'
            if skills.get("tools"):
                html_content += f'\n            <div class="skill-category"><strong>Инструменты:</strong> {", ".join(skills["tools"])}</div>'

            html_content += "\n        </div>\n    </div>"

        # Опыт и проекты
        experience = self.data.get("experience", [])
        if experience:
            html_content += '\n\n    <div class="section">\n        <h2><span class="emoji">💼</span>Опыт / Проекты</h2>'

            # Группировка по типам
            projects_by_type = {}
            for project in experience:
                project_type = project.get("type", "Проект")
                if project_type not in projects_by_type:
                    projects_by_type[project_type] = []
                projects_by_type[project_type].append(project)

            # Отображение групп проектов
            for project_type, projects in projects_by_type.items():
                if len(projects) > 1 or project_type != "Проект":
                    html_content += (
                        f"\n        <h3><strong>{project_type}</strong></h3>"
                    )

                for project in projects:
                    html_content += '\n        <div class="project">\n            <h3>'

                    # Название проекта как ссылка или простой текст
                    title = project.get("title", "Без названия")
                    if project.get("link"):
                        html_content += (
                            f'<a href="{project["link"]}" target="_blank">{title}</a>'
                        )
                    else:
                        html_content += title
                    html_content += "</h3>"

                    if project.get("description"):
                        html_content += f'\n            <p><strong>Описание:</strong> {project["description"]}</p>'
                    if project.get("tech_stack"):
                        html_content += f'\n            <div class="tech-stack"><strong>Стек:</strong> {", ".join(project["tech_stack"])}</div>'
                    if project.get("date"):
                        html_content += (
                            f'\n            <p class="date">({project["date"]})</p>'
                        )
                    html_content += "\n        </div>"

            html_content += "\n    </div>"

            html_content += "\n    </div>"

        # Образование
        education = self.data.get("education", {})
        if education:
            html_content += '\n\n    <div class="section">\n        <h2><span class="emoji">🎓</span>Образование</h2>\n'

            if isinstance(education, list):
                for edu in education:
                    html_content += '\n        <div class="project">'
                    if edu.get("institution"):
                        html_content += f'\n            <h3>{edu["institution"]}</h3>'
                    if edu.get("field"):
                        html_content += f'\n            <p><strong>Направление:</strong> {edu["field"]}</p>'
                    if edu.get("degree"):
                        html_content += f'\n            <p><strong>Степень:</strong> {edu["degree"]}</p>'
                    if edu.get("period"):
                        html_content += f'\n            <p>{edu["period"]}</p>'
                    html_content += "\n        </div>"
            else:
                # Обратная совместимость со старым форматом
                html_content += '\n        <div class="project">'
                if education.get("institution"):
                    html_content += f'\n            <h3>{education["institution"]}</h3>'
                if education.get("field"):
                    html_content += f'\n            <p><strong>Направление:</strong> {education["field"]}</p>'
                if education.get("period"):
                    html_content += f'\n            <p>{education["period"]}</p>'
                html_content += "\n        </div>"

            html_content += "\n    </div>"

        # Сертификаты
        certificates = self.data.get("certificates", [])
        if certificates:
            html_content += '\n\n    <div class="section">\n        <h2><span class="emoji">📜</span>Сертификаты и курсы</h2>\n        <ul>'
            for cert in certificates:
                html_content += f"\n            <li>{cert}</li>"
            html_content += "\n        </ul>\n    </div>"

        # Информация о генерации
        html_content += f'\n\n    <div class="generated-info">\n        Created by Oderiy Yaroslav CV Generator • {datetime.now().strftime("%d.%m.%Y")}\n    </div>'

        html_content += "\n</body>\n</html>"

        return html_content

    def build(self, output_dir="build"):
        """Сборка всех версий резюме"""
        # Создание директории для вывода
        Path(output_dir).mkdir(exist_ok=True)

        print("🚀 Начинаем сборку резюме...")

        # Генерация Markdown для GitHub Pages
        try:
            md_content = self.generate_markdown()
            with open("index.md", "w", encoding="utf-8") as f:
                f.write(md_content)
            print("✅ index.md обновлен для GitHub Pages")
        except Exception as e:
            print(f"❌ Ошибка при создании index.md: {e}")

        # Генерация standalone HTML
        try:
            html_content = self.generate_html()
            html_path = Path(output_dir) / "resume.html"
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(html_content)
            print(f"✅ Standalone HTML создан: {html_path}")
        except Exception as e:
            print(f"❌ Ошибка при создании HTML: {e}")

        # Копирование favicon
        if os.path.exists("favicon.ico"):
            try:
                import shutil

                shutil.copy2("favicon.ico", Path(output_dir) / "favicon.ico")
                print("✅ favicon.ico скопирован")
            except Exception as e:
                print(f"⚠️  Не удалось скопировать favicon.ico: {e}")

        print("\n🎉 Сборка завершена!")
        print(f"📁 Файлы созданы в: {os.path.abspath(output_dir)}")
        print(
            f"🌐 Откройте {os.path.abspath(output_dir)}/resume.html в браузере для предварительного просмотра"
        )
        print("📝 index.md готов для коммита в GitHub Pages")


def main():
    """Основная функция"""
    builder = ResumeBuilder()

    if not builder.data:
        print("❌ Не удалось загрузить данные. Проверьте файл resume_data.json")
        return

    builder.build()


if __name__ == "__main__":
    main()
