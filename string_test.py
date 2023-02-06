value = """<sup xmlns="http://www.w3.org/1999/xhtml">[<a href="javascript:open_code('CX')">CX</a>]</sup> <img xmlns="http://www.w3.org/1999/xhtml" border="0" alt="[Option Start]" src="../images/opt-start.gif" /> The
behavior is undefined if the <i xmlns="http://www.w3.org/1999/xhtml">locale</i> argument to <i xmlns="http://www.w3.org/1999/xhtml">isdigit_l</i>() is the special locale object LC_GLOBAL_LOCALE or is not a
valid locale object handle. <img xmlns="http://www.w3.org/1999/xhtml" border="0" alt="[Option End]" src="../images/opt-end.gif" />"""
value = value.replace('\'', "\"")
print(value)
test = f"""{value}"""
if f"""{test}""".find('"') > 0:
    print('it_works')