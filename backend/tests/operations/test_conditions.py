import pytest
import pandas as pd
from app.operations.conditions import (
    EqualsCondition, NotEqualsCondition, GreaterThanCondition,
    GreaterThanOrEqualsCondition, LessThanCondition, LessThanOrEqualsCondition,
    IsNullCondition, IsNotNullCondition, ContainsCondition,
    StartsWithCondition, EndsWithCondition, InCondition,
    AndCondition, OrCondition, NotCondition, IdentityCondition
)

# -- Comparison Conditions --

def test_equals_condition(sample_df):
    cond = EqualsCondition('city', 'Chicago')
    assert cond.apply(sample_df).sum() == 1
    assert cond.to_code() == "df['city'] == Chicago"

def test_not_equals_condition(sample_df):
    cond = NotEqualsCondition('city', 'Chicago')
    assert cond.apply(sample_df).sum() == 4
    assert cond.to_code() == "df['city'] != Chicago"

def test_greater_than_condition(sample_df):
    cond = GreaterThanCondition('salary', 70000)
    assert cond.apply(sample_df).sum() == 2
    assert cond.to_code() == "df['salary'] > 70000"

def test_greater_than_or_equals_condition(sample_df):
    cond = GreaterThanOrEqualsCondition('salary', 70000)
    assert cond.apply(sample_df).sum() == 3
    assert cond.to_code() == "df['salary'] >= 70000"

def test_less_than_condition(sample_df):
    cond = LessThanCondition('salary', 70000)
    assert cond.apply(sample_df).sum() == 2
    assert cond.to_code() == "df['salary'] < 70000"

def test_less_than_or_equals_condition(sample_df):
    cond = LessThanOrEqualsCondition('salary', 70000)
    assert cond.apply(sample_df).sum() == 3
    assert cond.to_code() == "df['salary'] <= 70000"

# -- Nullability Conditions --

def test_is_null_condition(sample_df):
    cond = IsNullCondition('age')
    assert cond.apply(sample_df).sum() == 1
    assert cond.to_code() == "df['age'].isnull()"

def test_is_not_null_condition(sample_df):
    cond = IsNotNullCondition('age')
    assert cond.apply(sample_df).sum() == 4
    assert cond.to_code() == "df['age'].notnull()"

# -- Identity Condition --

def test_identity_condition(sample_df):
    cond = IdentityCondition('active')
    assert cond.apply(sample_df).sum() == 3
    assert cond.to_code() == "df['active']"

# -- String Conditions --

def test_string_conditions(sample_df):
    c1 = ContainsCondition('city', 'New')
    assert c1.apply(sample_df).sum() == 1
    assert c1.to_code() == "df['city'].str.contains('New')"
    
    c2 = StartsWithCondition('city', 'L')
    assert c2.apply(sample_df).sum() == 1
    assert c2.to_code() == "df['city'].str.startswith('L')"

    c3 = EndsWithCondition('city', 'o')
    assert c3.apply(sample_df).sum() == 1  # Chicago
    assert c3.to_code() == "df['city'].str.endswith('o')"

def test_membership_condition(sample_df):
    cond = InCondition('city', ['Chicago', 'Houston'])
    assert cond.apply(sample_df).sum() == 2
    assert cond.to_code() == "df['city'].isin(['Chicago', 'Houston'])"

# -- Logical Conditions --

def test_logical_conditions(sample_df):
    c1 = GreaterThanCondition('age', 30)
    c2 = EqualsCondition('active', True)
    
    and_c = AndCondition(c1, c2)
    assert and_c.apply(sample_df).sum() == 1
    assert and_c.to_code() == "(df['age'] > 30) & (df['active'] == True)"
    
    or_c = OrCondition(c1, c2)
    assert or_c.apply(sample_df).sum() == 4
    assert or_c.to_code() == "(df['age'] > 30) | (df['active'] == True)"
    
    not_c = NotCondition(c2)
    assert not_c.apply(sample_df).sum() == 2
    assert not_c.to_code() == "~ (df['active'] == True)"
