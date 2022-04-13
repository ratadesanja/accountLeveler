PROCESS_NAME = 'League of Legends.exe'

oObjectManager = 0x24A4B90 #12.7
oObjectMapRoot = 0x28 #0x28
oObjectMapNodeNetId = 0x10
oObjectMapNodeObject = 0x14
 
OBJECT_SIZE = 0x3400
oObjectAbilityPower = 0x1750 #12.7
oObjectArmor = 0x12AC #12.7
oObjectAtkRange = 0x12CC #12.7
oObjectAtkSpeedMulti = 0x12B8
oObjectBaseAtk = 0x1284 #12.7
oObjectBonusAtk = 0x1234
oObjectHealth = 0xDB4
oObjectMaxHealth = oObjectHealth + 0x10
oObjectLevel = 0x33A0 #12.7
oObjectMagicRes = 0x12B4 #12.7
oObjectMana = 0x2B4 #12.7
oObjectPos = 0x23C #12.7
oObjectTeam = 0x4C #12.7
oObjectTargetable = 0xD1C #12.7
oObjectVisibility = 0x28C #12.7
oObjectInvulnerable = 0x3EC #12.7
oObjectName = 0x2BAC #12.7
oObjectNetworkID = 0xCC
oObjectSizeMultiplier = 0x12D4
oObjectSpawnCount = 0x2A0
oObjectSpellBook = 0x27AC #12.7 0x27C0
oObjectSpellBookArray = 0x488 #0x488 good offsets x478
oObjectBuffManager = 0x2180 #12.7
oObjectBuffManagerEntriesStart = oObjectBuffManager + 0x10
oObjectBuffManagerEntriesEnd = oObjectBuffManager + 0x14
 
SPELL_SIZE = 0x68 #60 works
oSpellSlotLevel = 0x1C #12.7
oSpellSlotCooldownExpire = 0x24 #12.7
oSpellSlotTime = 0x24 #12.7
oSpellSlotCharges = 0x54 #12.7
oSpellSlotTimeCharge = 0x74 #12.7
oSpellSlotDamage = 0x94 #12.7
oSpellSlotSpellInfo = 0x120 #12.7
oSpellInfoSpellData = 0x44
oSpellDataSpellName = 0x6C #12.7
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
 
oLocalPlayer = 0x30F5BBC #12.7
oViewProjMatrices = 0x31203A0 #12.7
oRenderer = 0x31232A0 #12.7
oRendererWidth = 0xC #12.5 #0x10
oRendererHeight = 0x10 #12.5 #0x14
oGameTime = 0x30ECC8C #12.7

oGold = 0x1b98