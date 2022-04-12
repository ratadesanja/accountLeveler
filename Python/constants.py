PROCESS_NAME = 'League of Legends.exe'

oObjectManager = 0x24B9BB0 #12.5
oObjectMapRoot = 0x28
oObjectMapNodeNetId = 0x10
oObjectMapNodeObject = 0x14
 
OBJECT_SIZE = 0x3400
oObjectAbilityPower = 0x1788
oObjectArmor = 0x12E4
oObjectAtkRange = 0x1304
oObjectAtkSpeedMulti = 0x12B8
oObjectBaseAtk = 0x12BC
oObjectBonusAtk = 0x1234
oObjectHealth = 0xDB4
oObjectMaxHealth = oObjectHealth + 0x10
oObjectLevel = 0x33A4
oObjectMagicRes = 0x12EC
oObjectMana = 0x2B4
oObjectPos = 0x1F4
oObjectTeam = 0x4C
oObjectTargetable = 0xD1C
oObjectVisibility = 0x28C
oObjectName = 0x2BE4
oObjectNetworkID = 0xCC
oObjectSizeMultiplier = 0x12D4
oObjectSpawnCount = 0x2A0
oObjectSpellBook = 0x27e4 #0x27e4 good offsets
oObjectSpellBookArray = 0x488 #0x488 good offsets
oObjectBuffManager = 0x21B8 #12.5
oObjectBuffManagerEntriesStart = oObjectBuffManager + 0x10
oObjectBuffManagerEntriesEnd = oObjectBuffManager + 0x14
 
SPELL_SIZE = 0x68 #60 works
oSpellSlotLevel = 0x20
oSpellSlotCooldownExpire = 0x28 #28 works????
oSpellSlotTime = 0x28
oSpellSlotCharges = 0x58
oSpellSlotTimeCharge = 0x78
oSpellSlotDamage = 0x98
oSpellSlotSpellInfo = 0x13C
oSpellInfoSpellData = 0x44
oSpellDataSpellName = 0x6C
oSpellDataMissileName = 0x6C
oSpellSlotSmiteTimer = 0x64
oSpellSlotSmiteCharges = 0x58

BUFF_SIZE = 0x78
oBuffInfo = 0x8
oBuffCount = 0x74
oBuffEndTime = 0x10
oBuffInfoName = 0x8
 
oObjectX = oObjectPos
oObjectZ = oObjectPos + 0x4
oObjectY = oObjectPos + 0x8
 
oLocalPlayer = 0x310B314 #12.5
oViewProjMatrices = 0x3135818 #12.5
oRenderer = 0x3138718 #12.5
oRendererWidth = 0xC #12.5 #0x10
oRendererHeight = 0x10 #12.5 #0x14
#oRendererWidth = 0xC #0x10
#oRendererHeight = 0x10 #0x14
oGameTime = 0x31023CC #12.6

oGold = 0x1b98