from django.core.management.base import BaseCommand
from codetests.models import Test, TestCase

class Command(BaseCommand):
    help = 'Create sample coding tests with test cases'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample tests...')

        # Test 1: Two Sum
        test1 = Test.objects.create(
            name="Two Sum",
            description="""Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

Example:
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].""",
            time_limit=30,
            difficulty="Easy"
        )

        TestCase.objects.create(
            test=test1,
            input_data="[2, 7, 11, 15]\n9",
            expected_output="[0, 1]",
            is_sample=True
        )

        TestCase.objects.create(
            test=test1,
            input_data="[3, 2, 4]\n6",
            expected_output="[1, 2]",
            is_sample=False
        )

        # Test 2: Palindrome Check
        test2 = Test.objects.create(
            name="Palindrome Checker",
            description="""Write a function that checks if a given string is a palindrome.

A palindrome is a word, phrase, number, or other sequence of characters that reads the same forward and backward (ignoring spaces, punctuation, and capitalization).

Example:
Input: "A man a plan a canal Panama"
Output: True

Input: "race a car"
Output: False""",
            time_limit=20,
            difficulty="Easy"
        )

        TestCase.objects.create(
            test=test2,
            input_data="racecar",
            expected_output="True",
            is_sample=True
        )

        TestCase.objects.create(
            test=test2,
            input_data="hello",
            expected_output="False",
            is_sample=False
        )

        # Test 3: Fibonacci Sequence
        test3 = Test.objects.create(
            name="Fibonacci Number",
            description="""Write a function to calculate the nth Fibonacci number.

The Fibonacci sequence is: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, ...

Where each number is the sum of the two preceding ones, starting from 0 and 1.

Example:
Input: n = 5
Output: 5

Input: n = 10
Output: 55""",
            time_limit=25,
            difficulty="Medium"
        )

        TestCase.objects.create(
            test=test3,
            input_data="5",
            expected_output="5",
            is_sample=True
        )

        TestCase.objects.create(
            test=test3,
            input_data="10",
            expected_output="55",
            is_sample=False
        )

        # Test 4: Binary Search
        test4 = Test.objects.create(
            name="Binary Search",
            description="""Implement binary search algorithm.

Given a sorted array of integers and a target value, return the index of the target if it exists, otherwise return -1.

You must write an algorithm with O(log n) runtime complexity.

Example:
Input: nums = [1,2,3,4,5,6,7,8,9], target = 6
Output: 5

Input: nums = [1,2,3,4,5], target = 6
Output: -1""",
            time_limit=35,
            difficulty="Medium"
        )

        TestCase.objects.create(
            test=test4,
            input_data="[1, 2, 3, 4, 5, 6, 7, 8, 9]\n6",
            expected_output="5",
            is_sample=True
        )

        TestCase.objects.create(
            test=test4,
            input_data="[1, 2, 3, 4, 5]\n6",
            expected_output="-1",
            is_sample=False
        )

        # Test 5: Reverse Linked List
        test5 = Test.objects.create(
            name="Reverse Linked List",
            description="""Given the head of a singly linked list, reverse the list and return the reversed list.

Example:
Input: 1 -> 2 -> 3 -> 4 -> 5
Output: 5 -> 4 -> 3 -> 2 -> 1

Input: 1 -> 2
Output: 2 -> 1""",
            time_limit=40,
            difficulty="Hard"
        )

        TestCase.objects.create(
            test=test5,
            input_data="[1, 2, 3, 4, 5]",
            expected_output="[5, 4, 3, 2, 1]",
            is_sample=True
        )

        TestCase.objects.create(
            test=test5,
            input_data="[1, 2]",
            expected_output="[2, 1]",
            is_sample=False
        )

        self.stdout.write(self.style.SUCCESS('Successfully created 5 sample tests with test cases!'))
        self.stdout.write(f'- {test1.name} ({test1.difficulty})')
        self.stdout.write(f'- {test2.name} ({test2.difficulty})')
        self.stdout.write(f'- {test3.name} ({test3.difficulty})')
        self.stdout.write(f'- {test4.name} ({test4.difficulty})')
        self.stdout.write(f'- {test5.name} ({test5.difficulty})')
