import flet as ft
from google import genai

# Initialize the modern Google GenAI Client
# Remember to paste your actual free Gemini API key string from Google AI Studio here!
client = genai.Client(api_key="YOUR_FREE_GEMINI_API_KEY")

def main(page: ft.Page):
    page.title = "Swapnil_AI_Search"
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO
    
    # Ensures the application layout scales cleanly to native mobile viewport screens
    page.window_width = 400
    page.window_height = 800

    # --- UI Layout Components ---
    header_text = ft.Text("Swapnil_AI_Search", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_ACCENT_400)
    subtitle_text = ft.Text("Search keywords, prompts, or pasted data streams directly", size=13, color=ft.Colors.GREY_400)

    search_input = ft.TextField(
        hint_text="Type context data or paste source snippets here...",
        multiline=True,
        min_lines=1,
        max_lines=4,
        expand=True,
        border_radius=10,
    )

    results_container = ft.Column(spacing=15, scroll=ft.ScrollMode.AUTO, expand=True)
    loading_indicator = ft.ProgressRing(visible=False, color=ft.Colors.BLUE_ACCENT_400)

    # --- Logic Execution Engine ---
    def execute_ai_search(e):
        query_text = search_input.value.strip()
        
        if not query_text:
            return

        loading_indicator.visible = True
        search_button.disabled = True
        page.update()
        
        try:
            results_container.controls.append(
                ft.Container(
                    content=ft.Text(f"🔍 Analyzing Context Prompt...", size=14, weight=ft.FontWeight.W_600),
                    padding=10, bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST, border_radius=8
                )
            )
            page.update()

            # FIX: Passed system_instruction directly as a root argument for seamless mobile SDK validation
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=query_text,
                system_instruction=(
                    "You are Swapnil_AI_Search, a multi-modal data processing assistant. "
                    "You have full capabilities to read text data, analyze technical audio scripts, "
                    "break down logs, handle camera snippets, and parse information tables. "
                    "Provide deeply factual, comprehensive, structured answers back to the user."
                )
            )
            
            results_container.controls.append(
                ft.Container(
                    content=ft.Markdown(
                        response.text, 
                        selectable=True, 
                        extension_set="gitHubWeb" # FIX: Converted to mobile-compatible string parameter
                    ),
                    padding=12, bgcolor=ft.Colors.SURFACE_CONTAINER, border_radius=8
                )
            )
            search_input.value = ""

        except Exception as err:
            results_container.controls.append(
                ft.Text(f"❌ Execution Failure: {str(err)}", color=ft.Colors.RED_ACCENT_400)
            )
        
        loading_indicator.visible = False
        search_button.disabled = False
        page.update()

    # --- Mobile-Safe Clipboard Actions Controller ---
    def handle_clipboard_paste(e):
        try:
            clipboard_contents = page.get_clipboard_data()
            if clipboard_contents:
                search_input.value = (search_input.value or "") + str(clipboard_contents)
                page.update()
        except Exception:
            search_input.hint_text = "Clipboard access restricted by device OS. Type directly instead."
            page.update()

    # --- Interactive Action Layout Assembly ---
    paste_button = ft.IconButton(
        icon=ft.Icons.CONTENT_PASTE_ROUNDED,
        icon_color=ft.Colors.BLUE_ACCENT_200,
        icon_size=26,
        tooltip="Paste data from clipboard",
        on_click=handle_clipboard_paste
    )

    search_button = ft.IconButton(
        icon=ft.Icons.SEARCH_ROUNDED,
        icon_color=ft.Colors.BLUE_ACCENT_400,
        icon_size=28,
        on_click=execute_ai_search
    )

    search_bar_row = ft.Row(
        controls=[paste_button, search_input, search_button],
        alignment=ft.MainAxisAlignment.CENTER
    )

    page.add(
        ft.Container(
            content=ft.Column(
                controls=[
                    header_text, subtitle_text, 
                    ft.Divider(height=15, color=ft.Colors.GREY_800),
                    search_bar_row,
                    ft.Row([loading_indicator], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                    results_container
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            padding=15, expand=True
        )
    )

if __name__ == "__main__":
    ft.run(main)
