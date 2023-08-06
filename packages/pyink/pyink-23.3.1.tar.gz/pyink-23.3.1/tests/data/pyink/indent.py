def abc():
  if True:
    some_very_long_function(
        param1=long_value1,
        param2=long_value2,
        param3=long_value3,
        param4=another_function_call(
            continued_param1=some_other_value1,
            continued_param2=some_other_value2,
            continued_param3=[
                something_in_the_list1,
                something_in_the_list2,
            ],
            continued_param4=(
                something_in_the_tuple1,
                something_in_the_tuple2,
            ),
            continued_param5={
                "some_key": "some_value",
            },
        ),
    )

  some_dict = {
      "some_key_1": {
          "sub_dict_key_1": "value1",
          "sub_dict_key_2": "value2",
          "sub_dict_key_3": "value3",
      },
      "some_key_2": "value2",
      "some_key_3": "value3",
  }
