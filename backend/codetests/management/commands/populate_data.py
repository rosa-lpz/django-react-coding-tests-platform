from django.core.management.base import BaseCommand
from codetests.models import Test, TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate the database with sample tests and test cases'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample data...')

        # Create a test user if it doesn't exist
        if not User.objects.filter(username='testuser').exists():
            User.objects.create_user(
                username='testuser',
                email='test@example.com',
                password='testpass123'
            )
            self.stdout.write(self.style.SUCCESS('Created test user: testuser/testpass123'))

        # Create sample tests
        test1 = Test.objects.create(
            name='Two Sum',
            description='''Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

Example:
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].''',
            time_limit=30,
            difficulty='Easy'
        )

        TestCase.objects.create(
            test=test1,
            input_data='[2,7,11,15]\n9',
            expected_output='[0, 1]',
            is_sample=True
        )

        TestCase.objects.create(
            test=test1,
            input_data='[3,2,4]\n6',
            expected_output='[1, 2]',
            is_sample=True
        )

        test2 = Test.objects.create(
            name='Palindrome Check',
            description='''Write a function that checks whether a given string is a palindrome.

A palindrome is a word, phrase, number, or other sequence of characters that reads the same forward and backward (ignoring spaces, punctuation, and capitalization).

Example:
Input: "A man a plan a canal Panama"
Output: True''',
            time_limit=20,
            difficulty='Easy'
        )

        TestCase.objects.create(
            test=test2,
            input_data='racecar',
            expected_output='True',
            is_sample=True
        )

        TestCase.objects.create(
            test=test2,
            input_data='hello',
            expected_output='False',
            is_sample=True
        )

        test3 = Test.objects.create(
            name='Reverse Linked List',
            description='''Given the head of a singly linked list, reverse the list, and return the reversed list.

Example:
Input: head = [1,2,3,4,5]
Output: [5,4,3,2,1]''',
            time_limit=45,
            difficulty='Medium'
        )

        TestCase.objects.create(
            test=test3,
            input_data='[1,2,3,4,5]',
            expected_output='[5,4,3,2,1]',
            is_sample=True
        )

        test4 = Test.objects.create(
            name='Binary Tree Maximum Path Sum',
            description='''A path in a binary tree is a sequence of nodes where each pair of adjacent nodes in the sequence has an edge connecting them. A node can only appear in the sequence at most once. Note that the path does not need to pass through the root.

The path sum of a path is the sum of the node's values in the path.

Given the root of a binary tree, return the maximum path sum of any non-empty path.''',
            time_limit=60,
            difficulty='Hard'
        )

        TestCase.objects.create(
            test=test4,
            input_data='[1,2,3]',
            expected_output='6',
            is_sample=True
        )

        self.stdout.write(self.style.SUCCESS('Successfully created sample tests and test cases!'))
        self.stdout.write(self.style.WARNING('Test user credentials: testuser / testpass123'))
