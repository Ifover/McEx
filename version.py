# UTF-8
#
# For more details about fixed file info 'ffi' see:
# http://msdn.microsoft.com/en-us/library/ms646997.aspx
VSVersionInfo(
  ffi=FixedFileInfo(
    # filevers and prodvers should be always a tuple with four items: (1, 2, 3, 4)
    # Set not needed items to zero 0.
    filevers=(2, 0, 3, 1029),
    prodvers=(2, 0, 3, 1029),
    # Contains a bitmask that specifies the valid bits 'flags'r
    mask=0x3f,
    # Contains a bitmask that specifies the Boolean attributes of the file.
    flags=0x0,
    # The operating system for which this file was designed.
    # 0x4 - NT and there is no need to change it.
    OS=0x40004,
    # The general type of file.
    # 0x1 - the file is an application.
    fileType=0x1,
    # The function of the file.
    # 0x0 - the function is not defined for this fileType
    subtype=0x0,
    # Creation date and time stamp.
    date=(0, 0)
    ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'080404b0',
        [StringStruct(u'CompanyName', u'Underwater Cubs'),
        StringStruct(u'FileDescription', u'魔法卡片超级无敌Super帅的换卡器'),
        StringStruct(u'FileVersion', u'2.0.3'),
        StringStruct(u'LegalCopyright', u'Copyright (C) 2020 Underwater Cubs. All Rights Reserved'),
        StringStruct(u'ProductName', u'Super McEx'),
        StringStruct(u'ProductVersion', u'2.0.3')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [2052, 1200])])
  ]
)
