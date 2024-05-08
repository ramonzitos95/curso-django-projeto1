from django.urls import reverse, resolve 
from recipes import views
from .recipe_test_base import RecipeTestBase
from unittest import skip
    
class RecipeHomeViewTest(RecipeTestBase):
    def test_recipe_home_views_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)
    
    def test_recipe_home_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)
    
    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')
        
    def test_recipe_home_shows_no_recipes_found_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        print(content)
        self.assertIn(
            '<h1>No recipes found here 🥲</h1>',
            content
        )
        #self.fail('Para que eu termine de digitá-lo')
        
    def test_recipe_home_template_loads_recipe(self):
        #need a recipe for this test
        self.make_recipe()
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']
        
        self.assertIn('Recipe Title', content)
        self.assertEqual(len(response_context_recipes), 1)

    def test_recipe_home_template_dont_load_recipes_not_published(self):
        """Test recipe is_published False dont show"""
        #need a recipe for this test
        self.make_recipe(is_published=False)
        
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        
        self.assertIn(
            '<h1>No recipes found here 🥲</h1>',
            content
        )
    