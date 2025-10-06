#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Интерактивный редактор резюме
Позволяет быстро редактировать данные резюме через консольный интерфейс
"""

import json
import os
from build_resume import ResumeBuilder


class ResumeEditor:
    def __init__(self, data_file="resume_data.json"):
        self.data_file = data_file
        self.builder = ResumeBuilder(data_file)
        self.data = self.builder.data.copy()

    def save_data(self):
        """Сохранение данных в JSON файл"""
        try:
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
            print("✅ Данные сохранены!")
            return True
        except Exception as e:
            print(f"❌ Ошибка при сохранении: {e}")
            return False

    def edit_personal_info(self):
        """Редактирование персональной информации"""
        print("\n=== Редактирование персональной информации ===")
        personal = self.data.setdefault("personal_info", {})

        print(f"Текущее имя: {personal.get('name', 'не указано')}")
        new_name = input("Новое имя (Enter для пропуска): ").strip()
        if new_name:
            personal["name"] = new_name

        print(f"Текущий email: {personal.get('email', 'не указан')}")
        new_email = input("Новый email (Enter для пропуска): ").strip()
        if new_email:
            personal["email"] = new_email

        print(f"Текущий Telegram: {personal.get('telegram', 'не указан')}")
        new_telegram = input("Новый Telegram (Enter для пропуска): ").strip()
        if new_telegram:
            if not new_telegram.startswith("@"):
                new_telegram = "@" + new_telegram
            personal["telegram"] = new_telegram

        print(f"Текущий GitHub: {personal.get('github', 'не указан')}")
        new_github = input("Новый GitHub (Enter для пропуска): ").strip()
        if new_github:
            personal["github"] = new_github

        print(f"Текущее местоположение: {personal.get('location', 'не указано')}")
        new_location = input("Новое местоположение (Enter для пропуска): ").strip()
        if new_location:
            personal["location"] = new_location

    def edit_skills(self):
        """Редактирование навыков"""
        print("\n=== Редактирование навыков ===")
        skills = self.data.setdefault("skills", {})

        categories = ["languages", "libraries", "tools"]
        category_names = ["Языки программирования", "Библиотеки", "Инструменты"]

        for cat, cat_name in zip(categories, category_names):
            print(f"\n{cat_name}:")
            current = skills.get(cat, [])
            print(f"Текущие: {', '.join(current) if current else 'не указаны'}")

            new_skills = input(
                f"Новые {cat_name.lower()} (через запятую, Enter для пропуска): "
            ).strip()
            if new_skills:
                skills[cat] = [
                    skill.strip() for skill in new_skills.split(",") if skill.strip()
                ]

    def add_project(self):
        """Добавление нового проекта"""
        print("\n=== Добавление нового проекта ===")

        title = input("Название проекта: ").strip()
        if not title:
            print("❌ Название проекта обязательно!")
            return

        print("Тип проекта:")
        print("1. Основной проект")
        print("2. Pet-проект")
        print("3. Хакатон")

        type_choice = input("Выберите тип (1-3): ").strip()
        type_map = {"1": "project", "2": "pet_project", "3": "hackathon"}
        project_type = type_map.get(type_choice, "pet_project")

        project = {"type": project_type, "title": title}

        link = input("Ссылка на проект (Enter для пропуска): ").strip()
        if link:
            project["link"] = link

        description = input("Описание проекта (Enter для пропуска): ").strip()
        if description:
            project["description"] = description

        tech_stack = input("Технологии (через запятую): ").strip()
        if tech_stack:
            project["tech_stack"] = [
                tech.strip() for tech in tech_stack.split(",") if tech.strip()
            ]

        date = input("Дата/период (например, 'лето 2025'): ").strip()
        if date:
            project["date"] = date

        experience = self.data.setdefault("experience", [])
        experience.append(project)

        print("✅ Проект добавлен!")

    def remove_project(self):
        """Удаление проекта"""
        print("\n=== Удаление проекта ===")
        experience = self.data.get("experience", [])

        if not experience:
            print("❌ Нет проектов для удаления!")
            return

        print("Текущие проекты:")
        for i, project in enumerate(experience):
            print(
                f"{i+1}. {project.get('title', 'Без названия')} ({project.get('type', 'неизвестно')})"
            )

        try:
            choice = int(input("Номер проекта для удаления (0 для отмены): ")) - 1
            if choice == -1:
                return
            if 0 <= choice < len(experience):
                removed = experience.pop(choice)
                print(f"✅ Проект '{removed.get('title')}' удален!")
            else:
                print("❌ Неверный номер проекта!")
        except ValueError:
            print("❌ Введите корректный номер!")

    def quick_add_skill(self):
        """Быстрое добавление навыка"""
        print("\n=== Быстрое добавление навыка ===")

        print("1. Язык программирования")
        print("2. Библиотека")
        print("3. Инструмент")

        choice = input("Категория (1-3): ").strip()
        category_map = {"1": "languages", "2": "libraries", "3": "tools"}
        category = category_map.get(choice)

        if not category:
            print("❌ Неверная категория!")
            return

        skill = input("Название навыка: ").strip()
        if not skill:
            print("❌ Название навыка не может быть пустым!")
            return

        skills = self.data.setdefault("skills", {})
        category_skills = skills.setdefault(category, [])

        if skill in category_skills:
            print(f"⚠️  Навык '{skill}' уже есть в списке!")
            return

        category_skills.append(skill)
        print(f"✅ Навык '{skill}' добавлен!")

    def preview_and_build(self):
        """Предварительный просмотр и сборка"""
        print("\n=== Предварительный просмотр и сборка ===")

        # Обновляем builder с новыми данными
        self.builder.data = self.data

        print("Сохраняем изменения...")
        if not self.save_data():
            return

        print("Собираем резюме...")
        self.builder.build()

        choice = input("\nОткрыть HTML версию в браузере? (y/n): ").strip().lower()
        if choice in ["y", "yes", "да", "д"]:
            try:
                import webbrowser

                html_path = os.path.abspath("build/resume.html")
                webbrowser.open(f"file://{html_path}")
                print("🌐 HTML версия открыта в браузере!")
            except Exception as e:
                print(f"❌ Не удалось открыть браузер: {e}")

    def show_menu(self):
        """Отображение главного меню"""
        print("\n" + "=" * 50)
        print("🔧 КОНСТРУКТОР РЕЗЮМЕ")
        print("=" * 50)
        print("1. Редактировать персональную информацию")
        print("2. Редактировать навыки")
        print("3. Добавить проект")
        print("4. Удалить проект")
        print("5. Быстро добавить навык")
        print("6. Предварительный просмотр и сборка")
        print("7. Сохранить и выйти")
        print("0. Выйти без сохранения")
        print("=" * 50)

    def run(self):
        """Запуск интерактивного редактора"""
        print("🚀 Добро пожаловать в конструктор резюме!")

        while True:
            self.show_menu()
            choice = input("Выберите действие (0-7): ").strip()

            if choice == "1":
                self.edit_personal_info()
            elif choice == "2":
                self.edit_skills()
            elif choice == "3":
                self.add_project()
            elif choice == "4":
                self.remove_project()
            elif choice == "5":
                self.quick_add_skill()
            elif choice == "6":
                self.preview_and_build()
            elif choice == "7":
                if self.save_data():
                    print("👋 До свидания!")
                    break
            elif choice == "0":
                confirm = input("Выйти без сохранения? (y/n): ").strip().lower()
                if confirm in ["y", "yes", "да", "д"]:
                    print("👋 До свидания!")
                    break
            else:
                print("❌ Неверный выбор! Попробуйте еще раз.")


def main():
    """Основная функция"""
    editor = ResumeEditor()
    editor.run()


if __name__ == "__main__":
    main()
