# -*- coding:utf-8 -*-
import phonenumbers

text = 'call me at 5713931405 is an gb number'

for match in phonenumbers.PhoneNumberMatcher(text, 'IN'):
    print(match.number)#, type(match), match.number, type(match.number))
    print(phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.NATIONAL))

phonenumbers.is_number_match('5713931405', '15713931405')
# print(phonenumbers.format_number(phonenumbers.parse('008615951993422', 'CN'), phonenumbers.PhoneNumberFormat.INTERNATIONAL))
# print(phonenumbers.format_number(phonenumbers.parse('+8615951993422', 'CN'), phonenumbers.PhoneNumberFormat.INTERNATIONAL))
# print(phonenumbers.format_number(phonenumbers.parse('15951993422', 'CN'), phonenumbers.PhoneNumberFormat.INTERNATIONAL))
#
# print(phonenumbers.format_number(phonenumbers.parse('2252542523', 'US'), phonenumbers.PhoneNumberFormat.INTERNATIONAL))
# print(phonenumbers.format_number(phonenumbers.parse('012252542523', 'US'), phonenumbers.PhoneNumberFormat.INTERNATIONAL))
# print(phonenumbers.format_number(phonenumbers.parse('+12252542523', 'US'), phonenumbers.PhoneNumberFormat.INTERNATIONAL))
