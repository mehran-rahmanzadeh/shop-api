from rest_framework.test import APITestCase
from django.urls import reverse_lazy
from django.db import IntegrityError, transaction

from categories.models import Category


class TestCategory(APITestCase):
    """Test category
    model test
    api endpoints test
    """

    def setUp(self):
        self.title = 'Mobile'
        self.slug = 'mobile'
        self.description = 'Lorem ipsum dolor sit amet, consecrate disciplining elit.'
        self.parent = None
        self.order = 1
        self.image = None
        self.category = self.create_category(
            title=self.title,
            slug=self.slug,
            description=self.description,
            parent=self.parent,
            order=self.order,
            image=self.image
        )

    @staticmethod
    def create_category(title, slug, description, parent, order, image):
        return Category.objects.create(
            title=title,
            slug=slug,
            description=description,
            parent=parent,
            order=order,
            image=image
        )

    def test_create_category_success(self):
        """Test create category"""
        title = 'Laptop'
        slug = 'laptop'
        description = 'Lorem ipsum dolor sit amet, consecrate disciplining elit.'
        parent = None
        order = 1
        image = None
        category = self.create_category(
            title=title, slug=slug,
            description=description, parent=parent,
            order=order, image=image
        )
        self.assertEqual(category.title, title)
        self.assertEqual(category.slug, slug)
        self.assertEqual(category.description, description)
        self.assertEqual(category.parent, parent)
        self.assertEqual(category.order, order)
        self.assertEqual(category.image, image)

    def test_create_category_slug_duplicated(self):
        """Test create category with duplicated slug"""
        title = 'Mobile'
        slug = self.slug
        description = 'Lorem ipsum dolor sit amet, consecrate disciplining elit.'
        parent = None
        order = 1
        image = None
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                _ = self.create_category(
                    title=title, slug=slug,
                    description=description,
                    parent=parent, order=order,
                    image=image
                )
        self.assertEqual(Category.objects.count(), 1)

    def test_list_category(self):
        """Test list category
        """
        url = reverse_lazy('category-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['title'], self.title)
        self.assertEqual(response.data['results'][0]['slug'], self.slug)
        self.assertEqual(response.data['results'][0]['description'], self.description)
        self.assertEqual(response.data['results'][0]['order'], self.order)
        self.assertEqual(response.data['results'][0]['image'], self.image)

    def test_filter_category_by_parent(self):
        """Test filter category by parent
        """
        title = 'Apple'
        slug = 'apple'
        description = 'Lorem ipsum dolor sit amet, consecrate disciplining elit.'
        parent = self.category
        order = 1
        image = None
        child = self.create_category(
            title=title,
            slug=slug,
            description=description,
            parent=parent,
            order=order,
            image=image
        )
        url = reverse_lazy('category-list')
        url += '?parent={}'.format(self.category.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['title'], title)
        self.assertEqual(response.data['results'][0]['slug'], slug)
        self.assertEqual(response.data['results'][0]['description'], description)
        self.assertEqual(response.data['results'][0]['order'], order)
        self.assertEqual(response.data['results'][0]['image'], image)

    def test_retrieve_category(self):
        """Test retrieve category
        """
        url = reverse_lazy('category-detail', kwargs={'pk': self.category.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], self.title)
        self.assertEqual(response.data['slug'], self.slug)
        self.assertEqual(response.data['description'], self.description)
        self.assertEqual(response.data['order'], self.order)
        self.assertEqual(response.data['image'], self.image)
