#canopen的cobid, rpto和rpdo是从servo的角度描述的.
cobid_EMCY  = 0x080
cobid_TSDO  = 0x600
cobid_RSDO  = 0x580
cobid_TPDO1 = 0x180
cobid_RPDO1 = 0x200
cobid_TPDO2 = 0x280
cobid_RPDO2 = 0x300
cobid_TPDO3 = 0x380
cobid_RPDO3 = 0x400
cobid_TPDO4 = 0x480
cobid_RPDO4 = 0x500
cobid_NMT   = '000'
cobid_HBEAT = 0x700
cobid_NODEG = 0x700
cobid_SYNC  = 0x080
#快速SDO,读写
sdo_w_1byte         = '2F'  #写1个byte
sdo_w_2byte         = '2B'  #写2个byte
sdo_w_3byte         = '27'  #写3个byte
sdo_w_4byte         = '23'  #写4个byte
sdo_w_rspd          = '60'  #写成功的回应
sdo_r               = '40'  #读,不管几个byte
sdo_rspd            = '42'  #返回的没有提示byte数量.
sdo_rspd_1byte      = '4F'  #读回1个byte
sdo_rspd_2byte      = '4B'  #读回2个byte   
sdo_rspd_3byte      = '47'  #读回3个byte
sdo_rspd_4byte      = '43'  #读回4个byte
sdo_rspd_abortion   = '80'  #读/写失败的回应
#segment sdo

#block sdo, write是download, r是upload
#以下几个用于发送
block_w_inil_crc    = 'C6'
block_w_inil        = 'C2'
block_w_end_7byte   = 'C1'  #最后一个block的segment里面7个byte都有效
block_w_end_6byte   = 'C5'  #最后一个block的segment里面6个byte都有效
block_w_end_5byte   = 'C9'  #最后一个block的segment里面5个byte都有效
block_w_end_4byte   = 'CD'  #最后一个block的segment里面4个byte都有效
block_w_end_3byte   = 'D1'  #最后一个block的segment里面3个byte都有效
block_w_end_2byte   = 'D5'  #最后一个block的segment里面2个byte都有效
block_w_end_1byte   = 'D9'  #最后一个block的segment里面1个byte都有效
block_w_end_0byte   = 'DD'  #最后一个block的segment里面0个byte都有效

block_r_init_p1_crc = 'A4'
block_r_inil_p1     = 'A0'  #block upload的initial的phase1
block_r_inil_p2     = 'A3'  #block upload的initial的phase2
block_r_sub         = 'A2'  #block upload的sub block
block_r_end         = 'A1'  #block uplaod的end
#以下几个用于接收后的判断
block_rspd_w_init_crc     = 'A4'  #download init的回应,支持crc
block_rspd_w_inil         = 'A0'  #download init的回应,不支持crc  
block_rspd_w_sub          = 'A2'  #block upload的sub block
block_rspd_w_end          = 'A1'  #block uplaod的end






nmt_operational     = '01'
nmt_stopmode        = '02'
nmt_preoperational  = '80'
nmt_resetnode       = '81'
nmt_resetcomm       = '82'

cmd_reboot          = '999'
cmd_update_trigger  = '981'
cmd_update_data     = '982'
cmd_update_crc      = '983'
cmd_update_status   = '984'

cmd_can_update      = '901'
cmd_od_config       = '902'
cmd_version         = '903'    
cmd_other_nodeid    = '904' 

cmd_csp_toggle      = '910'
cmd_csp_update      = '911'

cmd_csv_toggle      = '920'
cmd_csv_update      = '921'

cmd_cst_toggle      = '930'
cmd_cst_update      = '931'

cmd_alter_data1     = '941'
cmd_alter_data2     = '942'
cmd_alter_toggle    = '943'

cmd_ip_toggle       = '950'
cmd_ip_update       = '951'

cmd_pp_toggle       = '960'
cmd_pp_update       = '961'
cmd_pv_toggle       = '962'
cmd_pv_update       = '963'
cmd_pt_toggle       = '964'
cmd_pt_update       = '965'

rcvFrameIndex_Num   = 0
rcvFrameIndex_Time  = 1
rcvFrameIndex_TR    = 2
rcvFrameIndex_Rtr   = 3
rcvFrameIndex_Cobid = 4
rcvFrameIndex_Len   = 5
rcvFrameIndex_Data  = 6
rcvFrameMaxIndex    = 7

#defaultTimeGap
defaultTimeGap      = '3E8'        #0x3E8=1000us=1ms
#defaultTimeGap      = '190'        #0x190=400us=0.4ms
#defaultTimeGap      = '12C'        #0x12C=300us=0.3ms
defaultRtr          = '0'

#1006 communication cycle time
readCommunicationCycleTime      = '40061000'
writeCommunicationCycleTime     = '23061000'
#1009 hardware version
readManufactureHardwareVersionByte1  = '40091001'
readManufactureHardwareVersionByte2  = '40091002'
readManufactureHardwareVersionByte3  = '40091003'
readManufactureHardwareVersionByte4  = '40091004'
#100A software version
readManufactureSoftwareVersionByte1  = '400A1001'
readManufactureSoftwareVersionByte2  = '400A1002'
readManufactureSoftwareVersionByte3  = '400A1003'
readManufactureSoftwareVersionByte4  = '400A1004'
#1010 store parameters
writeStoreParameterSaveAll      = '23101001'
writeStoreParameterSaveComm     = '23101002'
writeStoreParameterSaveConfig   = '23101003'  
#1011 restore parameters
writeRestoreParameterAll      = '23111001'
writeRestoreParameterComm     = '23111002'
writeRestoreParameterConfig   = '23111003' 
#1017 producer heartbeat time
readProducerHeartbeatTime       = '40171000'
writeProducerHeartbeatTime      = '2B171000'
#1018 identity
readIdentitySerialNumber        = '40181004'
writeIdentitySerialNumber       = '23181004'
#1019 synchronousCounterOverflowValue
readSynchronousCounterOverflowValue       = '40191000'
writeSynchronousCounterOverflowValue      = '2F191000'
#rpdo1
readRPDO1Cobid                  = '40001401'
writeRPDO1Cobid                 = '23001401'
readRPDO1TransmissionType       = '40001402'
writeRPDO1TransmissionType      = '2F001402'
readRPDO1EventTimer             = '40001405'
writeRPDO1EventTimer            = '2B001405'
#rpdo2
readRPDO2Cobid                  = '40011401'
writeRPDO2Cobid                 = '23011401'
readRPDO2TransmissionType       = '40011402'
writeRPDO2TransmissionType      = '2F011402'
readRPDO2EventTimer             = '40011405'
writeRPDO2EventTimer            = '2B011405'
#rpdo3
readRPDO3Cobid                  = '40021401'
writeRPDO3Cobid                 = '23021401'
readRPDO3TransmissionType       = '40021402'
writeRPDO3TransmissionType      = '2F021402'
readRPDO3EventTimer             = '40021405'
writeRPDO3EventTimer            = '2B021405'
#rpdo4
readRPDO4Cobid                  = '40031401'
writeRPDO4Cobid                 = '23031401'
readRPDO4TransmissionType       = '40031402'
writeRPDO4TransmissionType      = '2F031402'
readRPDO4EventTimer             = '40031405'
writeRPDO4EventTimer            = '2B031405'
#rpdo1
readRPDO1NumberOfMappedObjects  = '40001600'
writeRPDO1NumberOfMappedObjects = '2F001600'
readRPDO1MappedObject1          = '40001601'
writeRPDO1MappedObject1         = '23001601'
readRPDO1MappedObject2          = '40001602'
writeRPDO1MappedObject2         = '23001602'
readRPDO1MappedObject3          = '40001603'
writeRPDO1MappedObject3         = '23001603'
readRPDO1MappedObject4          = '40001604'
writeRPDO1MappedObject4         = '23001604'
readRPDO1MappedObject3          = '40001605'
writeRPDO1MappedObject5         = '23001605'
readRPDO1MappedObject6          = '40001606'
writeRPDO1MappedObject6         = '23001606'
readRPDO1MappedObject7          = '40001607'
writeRPDO1MappedObject7         = '23001607'
readRPDO1MappedObject8          = '40001608'
writeRPDO1MappedObject8         = '23001608'
#rpdo2
readRPDO2NumberOfMappedObjects  = '40011600'
writeRPDO2NumberOfMappedObjects = '2F011600'
readRPDO2MappedObject1          = '40011601'
writeRPDO2MappedObject1         = '23011601'
readRPDO2MappedObject2          = '40011602'
writeRPDO2MappedObject2         = '23011602'
readRPDO2MappedObject3          = '40011603'
writeRPDO2MappedObject3         = '23011603'
readRPDO2MappedObject4          = '40011604'
writeRPDO2MappedObject4         = '23011604'
readRPDO2MappedObject3          = '40011605'
writeRPDO2MappedObject5         = '23011605'
readRPDO2MappedObject6          = '40011606'
writeRPDO2MappedObject6         = '23011606'
readRPDO2MappedObject7          = '40011607'
writeRPDO2MappedObject7         = '23011607'
readRPDO2MappedObject8          = '40011608'
writeRPDO2MappedObject8         = '23011608'
#rpdo3
readRPDO3NumberOfMappedObjects  = '40021600'
writeRPDO3NumberOfMappedObjects = '2F021600'
readRPDO3MappedObject1          = '40021601'
writeRPDO3MappedObject1         = '23021601'
readRPDO3MappedObject2          = '40021602'
writeRPDO3MappedObject2         = '23021602'
readRPDO3MappedObject3          = '40021603'
writeRPDO3MappedObject3         = '23021603'
readRPDO3MappedObject4          = '40021604'
writeRPDO3MappedObject4         = '23021604'
readRPDO3MappedObject3          = '40021605'
writeRPDO3MappedObject5         = '23021605'
readRPDO3MappedObject6          = '40021606'
writeRPDO3MappedObject6         = '23021606'
readRPDO3MappedObject7          = '40021607'
writeRPDO3MappedObject7         = '23021607'
readRPDO3MappedObject8          = '40021608'
writeRPDO3MappedObject8         = '23021608'
#rpdo4
readRPDO4NumberOfMappedObjects  = '40031600'
writeRPDO4NumberOfMappedObjects = '2F031600'
readRPDO4MappedObject1          = '40031601'
writeRPDO4MappedObject1         = '23031601'
readRPDO4MappedObject2          = '40031602'
writeRPDO4MappedObject2         = '23031602'
readRPDO4MappedObject3          = '40031603'
writeRPDO4MappedObject3         = '23031603'
readRPDO4MappedObject4          = '40031604'
writeRPDO4MappedObject4         = '23031604'
readRPDO4MappedObject3          = '40031605'
writeRPDO4MappedObject5         = '23031605'
readRPDO4MappedObject6          = '40031606'
writeRPDO4MappedObject6         = '23031606'
readRPDO4MappedObject7          = '40031607'
writeRPDO4MappedObject7         = '23031607'
readRPDO4MappedObject8          = '40031608'
writeRPDO4MappedObject8         = '23031608'
#tpdo1
readTPDO1Cobid                  = '40001801'
writeTPDO1Cobid                 = '23001801'
readTPDO1TransmissionType       = '40001802'
writeTPDO1TransmissionType      = '2F001802'
readTPDO1InhibitTime            = '40001803'
writeTPDO1InhibitTime           = '2B001803'
readTPDO1EventTimer             = '40001805'
writeTPDO1EventTimer            = '2B001805'
readTPDO1SyncStartValue         = '40001806'
writeTPDO1SyncStartValue        = '2F001806'
#tpdo2
readTPDO2Cobid                  = '40011801'
writeTPDO2Cobid                 = '23011801'
readTPDO2TransmissionType       = '40011802'
writeTPDO2TransmissionType      = '2F011802'
readTPDO2InhibitTime            = '40011803'
writeTPDO2InhibitTime           = '2B011803'
readTPDO2EventTimer             = '40011805'
writeTPDO2EventTimer            = '2B011805'
readTPDO2SyncStartValue         = '40011806'
writeTPDO2SyncStartValue        = '2F011806'
#tpdo3
readTPDO3Cobid                  = '40021801'
writeTPDO3Cobid                 = '23021801'
readTPDO3TransmissionType       = '40021802'
writeTPDO3TransmissionType      = '2F021802'
readTPDO3InhibitTime            = '40021803'
writeTPDO3InhibitTime           = '2B021803'
readTPDO3EventTimer             = '40021805'
writeTPDO3EventTimer            = '2B021805'
readTPDO3SyncStartValue         = '40021806'
writeTPDO3SyncStartValue        = '2F021806'
#tpdo4
readTPDO4Cobid                  = '40031801'
writeTPDO4Cobid                 = '23031801'
readTPDO4TransmissionType       = '40031802'
writeTPDO4TransmissionType      = '2F031802'
readTPDO4InhibitTime            = '40031803'
writeTPDO4InhibitTime           = '2B031803'
readTPDO4EventTimer             = '40031805'
writeTPDO4EventTimer            = '2B031805'
readTPDO4SyncStartValue         = '40031806'
writeTPDO4SyncStartValue        = '2F031806'
#tpdo1
readTPDO1NumberOfMappedObjects  = '40001A00'
writeTPDO1NumberOfMappedObjects = '2F001A00'
readTPDO1MappedObject1          = '40001A01'
writeTPDO1MappedObject1         = '23001A01'
readTPDO1MappedObject2          = '40001A02'
writeTPDO1MappedObject2         = '23001A02'
readTPDO1MappedObject3          = '40001A03'
writeTPDO1MappedObject3         = '23001A03'
readTPDO1MappedObject4          = '40001A04'
writeTPDO1MappedObject4         = '23001A04'
readTPDO1MappedObject3          = '40001A05'
writeTPDO1MappedObject5         = '23001A05'
readTPDO1MappedObject6          = '40001A06'
writeTPDO1MappedObject6         = '23001A06'
readTPDO1MappedObject7          = '40001A07'
writeTPDO1MappedObject7         = '23001A07'
readTPDO1MappedObject8          = '40001A08'
writeTPDO1MappedObject8         = '23001A08'
#tpdo2
readTPDO2NumberOfMappedObjects  = '40011A00'
writeTPDO2NumberOfMappedObjects = '2F011A00'
readTPDO2MappedObject1          = '40011A01'
writeTPDO2MappedObject1         = '23011A01'
readTPDO2MappedObject2          = '40011A02'
writeTPDO2MappedObject2         = '23011A02'
readTPDO2MappedObject3          = '40011A03'
writeTPDO2MappedObject3         = '23011A03'
readTPDO2MappedObject4          = '40011A04'
writeTPDO2MappedObject4         = '23011A04'
readTPDO2MappedObject3          = '40011A05'
writeTPDO2MappedObject5         = '23011A05'
readTPDO2MappedObject6          = '40011A06'
writeTPDO2MappedObject6         = '23011A06'
readTPDO2MappedObject7          = '40011A07'
writeTPDO2MappedObject7         = '23011A07'
readTPDO2MappedObject8          = '40011A08'
writeTPDO2MappedObject8         = '23011A08'
#tpdo3
readTPDO3NumberOfMappedObjects  = '40021A00'
writeTPDO3NumberOfMappedObjects = '2F021A00'
readTPDO3MappedObject1          = '40021A01'
writeTPDO3MappedObject1         = '23021A01'
readTPDO3MappedObject2          = '40021A02'
writeTPDO3MappedObject2         = '23021A02'
readTPDO3MappedObject3          = '40021A03'
writeTPDO3MappedObject3         = '23021A03'
readTPDO3MappedObject4          = '40021A04'
writeTPDO3MappedObject4         = '23021A04'
readTPDO3MappedObject3          = '40021A05'
writeTPDO3MappedObject5         = '23021A05'
readTPDO3MappedObject6          = '40021A06'
writeTPDO3MappedObject6         = '23021A06'
readTPDO3MappedObject7          = '40021A07'
writeTPDO3MappedObject7         = '23021A07'
readTPDO3MappedObject8          = '40021A08'
writeTPDO3MappedObject8         = '23021A08'
#tpdo4
readTPDO4NumberOfMappedObjects  = '40031A00'
writeTPDO4NumberOfMappedObjects = '2F031A00'
readTPDO4MappedObject1          = '40031A01'
writeTPDO4MappedObject1         = '23031A01'
readTPDO4MappedObject2          = '40031A02'
writeTPDO4MappedObject2         = '23031A02'
readTPDO4MappedObject3          = '40031A03'
writeTPDO4MappedObject3         = '23031A03'
readTPDO4MappedObject4          = '40031A04'
writeTPDO4MappedObject4         = '23031A04'
readTPDO4MappedObject3          = '40031A05'
writeTPDO4MappedObject5         = '23031A05'
readTPDO4MappedObject6          = '40031A06'
writeTPDO4MappedObject6         = '23031A06'
readTPDO4MappedObject7          = '40031A07'
writeTPDO4MappedObject7         = '23031A07'
readTPDO4MappedObject8          = '40031A08'
writeTPDO4MappedObject8         = '23031A08'
#1F50 boot, 这个是doumain，不在使用快速SDO了，使用BLOCK的关键字。
writeBootData                   = 'C2501F00'
writeBootData_CRC               = 'C6501F00'
#nmt startup
readNMTStartup                  = '40801F00'    
writeNMTStartup                 = '23801F00'    
#2000,system config
#修改后,参数配置改到0x1010去了.
#2001 canopen config
readCanopenConfigCanNodeid  = '40012001'
writeCanopenConfigCanNodeid = '2F012001'
readCanopenConfigCanBitrate  = '40012002'
writeCanopenConfigCanBitrate = '2B012002'
readCanopenConfigEnResistor  = '40012003'
writeCanopenConfigEnResistor = '2F012003'
#2003 ppr
readCprCountPerResolution     = '40032001'
writeCprCountPerResolution    = '23032001'
#2010, current pid
readPidIqKpGain_S         = '40102003'
writePidIqKpGain_S        = '23102003'
readPidIqKiGain_S         = '40102004'
writePidIqKiGain_S        = '23102004'
readPidIqAutoTuneTrigger  = '40102006'
writePidIqAutoTuneTrigger = '2F102006'

#2012, velocity pid
readPidVelocityKpGain_S         = '40122003'
writePidVelocityKpGain_S        = '23122003'
readPidVelocityKiGain_S         = '40122004'
writePidVelocityKiGain_S        = '23122004'
readPidVelocityStiffness        = '40122005'
writePidVelocityStiffness       = '23122005'
readPidVelocityAutoTuneTrigger  = '40122006'
writePidVelocityAutoTuneTrigger = '2F122006'
#2013, position pid
readPidPositionKpGain_S         = '40132002'
writePidPositionKpGain_S        = '23132002'
readPidPositionAutoTuneTrigger  = '40132003'
writePidPositionAutoTuneTrigger = '2F132003'
#2014 brake related
readBrakeRelatedAutoBrake       = '40142004'
writeBrakeRelatedAutoBrake      = '2F142004'
#2015 control strategy
readControlStrategyStepdirPosWithoutCanopen       = '40152005'
writeControlStrategyStepdirPosWithoutCanopen      = '2F152005'
readControlStrategyStepdirVelWithoutCanopen       = '40152006'
writeControlStrategyStepdirVelWithoutCanopen      = '2F152006'
#2016 filter
#2016 velocity filter bandwidth
readVelocityFilterBandwith      = '40162001' 
writeVelocityFilterBandwith     = '23162001'
#2017 iit
readIitLimit                    = '40172001'
writeIitlimit                   = '23172001'
readIitTrigLevel                = '40172003'
writeIitTrigLevel               = '23172003'
#2030 torque window
readTorqueWindow                = '40302000'
writeTorqueWindow               = '2B302000'
#2031 torque window timeout
readTorqueWindowTimeout         = '40312000'
writeTorqueWindowTimeout        = '2B312000'
#2034 internal target reach window
readInternalTargetReachWindow   = '40342000'
writeInternalTargetReachWindow  = '2B342000'
#203A block
readBlockTriggerCurrent     = '403A2001'
writeBlockTriggerCurrent    = '233A2001'
readBlockDuration           = '403A2002'
writeBlockDuration          = '2B3A2002'
#203B switch
readSwitchType              = '403B2001'
writeSwitchType             = '233B2001'
#2240 digital input control
readSpecialInputEnable      = '40402201'
writeSpecialInputEnable     = '23402201'
readSpecialInputReverse     = '40402202'
writeSpecialInputReverse    = '23402202'
#2250 digital output control
readSpecialOutputEnable      = '40502201'
writeSpecialOutputEnable     = '23502201'
readSpecialOutputReverse     = '40502202'
writeSpecialOutputReverse    = '23502202'
#4040 bootcontrol 4byte.
readBootRequest             = '40404000'
writeBootRequest            = '23404000'
bootRequestPassward         = '74647075'          #updt =  u=75,p=70,d=64,t=74
#6040 control word
readControlWrod             = '40406000'
writeControlWord            = '2B406000'
cw_shutDown                 = '06'
cw_switchOn                 = '07'
cw_disableVoltage           = '00'
cw_quickStop                = '02'
cw_disableOperation         = '07'
cw_enableOperation          = '0F'
cw_faultReset               = '80'
cw_halt                     = '010F'
cw_startHoming              = '1F'
cw_stopHoming               = '0F'
cw_nsp_relative_immediate    = '7F'            #相对位置,立即执行
cw_nsp_relative_notimmediate = '5F'            #相对位置,不立即执行
cw_nsp_absolute_immediate    = '3F'            #绝对位置,立即执行
cw_nsp_absolute_notimmediate = '1F'            #绝对位置,不立即执行
#6041 status word
statusWord                  = '0'
statusWord_Index            = '6041'
#6060 control mode
readControlMode             = '40606000'
writeControlMode            = '2F606000' 
mode_ppm                    = '01'
mode_pvm                    = '03'
mode_ptm                    = '04'
mode_hm                     = '06'
mode_ipm                    = '07'
mode_cspm                   = '08'
mode_csvm                   = '09'
mode_cstm                   = '0A'
#6064 position actual value
positionActualValue         = ''
positionActualValue_Index   = '6064'
#6065 following error window
readFollowingErrorWindow    = '40656000'
writeFollowingErrorWindow   = '23656000'
#6066 following error timeout
readFollowingErrorTimeout   = '40666000'
writeFollowingErrorTimeout  = '2B666000'
#6067 position window
readPositionWindow          = '40676000'
writePositionWindow         = '23676000'
#6068 position window time
readPositionWindowTime      = '40686000'
writePositionWindowTime     = '2B686000'
#606C velocityActualValue
velocityActualValue         = ''    
velocityActualValue_Index   = '606C'
#6071 target torque
readTargetTorque            = '40716000'
writeTargetTorque           = '2b716000'
#6072 max torque
readMaxTorque               = '40726000'
writeMaxTorque              = '2b726000'
#607A target position
readTargetPosition          = '407A6000'
writeTargetPosition         = '237A6000'
#607C home offset
readHomeOffset              = '407C6000'
writeHomeOffset             = '237C6000'
#607D software position limit
readMinPositionLimit          = '407D6001'
writeMinPositionLimit         = '237D6001'
readMaxPositionLimit          = '407D6002'
writeMaxPositionLimit         = '237D6002'
#607E polarity
readPolarity                = '407E6000'
writePolarity               = '2F7E6000'   
#607F max profile velocity
readMaxProfileVelocity      = '407F6000'
writeMaxProfileVelocity     = '237F6000'
#6081 profile velocity
readProfileVelocity         = '40816000'
writeProfileVelocity        = '23816000'
#6083 profile acceleration
readProfileAcceleration     = '40836000'
writeProfileAcceleration    = '23836000'
#6084 profile deceleration
readProfileDeceleration     = '40846000'
writeProfileDeceleration    = '23846000'
#6085 quickstop deceleration
readQuickstopDeceleration   = '40856000'
writeQuickstopDeceleration  = '23856000'
#6087 torque slope
readTorqueSlope             = '40876000'
writeTorqueSlope            = '23876000'
#6093 position factor
readPositionFactorNumerator     = '40936001'
writePositionFactorNumerator    = '23936001'
readPositionFactorDivisor       = '40936002'
writePositionFactorDivisor      = '23936002'
#6095 velocityfactor
readVelocityFactorNumerator     = '40956001'
writeVelocityFactorNumerator    = '23956001'
readVelocityFactorDivisor       = '40956002'
writeVelocityFactorDivisor      = '23956002'
#6097 acceleration factor
readAccelerationFactorNumerator   = '40976001'
writeAccelerationFactorNumerator  = '23976001' 
readAccelerationFactorDivisor     = '40976002'
writeAccelerationFactorDivisor    = '23976002'
#6098 homing method, 1byte
readHomingMethod                = '40986000'
writeHomingMethod               = '2F986000'
#6099 homing speed, 4byte
readHomingSpeed1                = '40996001'
writeHomingSpeed1               = '23996001'
readHomingSpeed2                = '40996002'
writeHomingSpeed2               = '23996002'
#609A homing acceleration
readHomingAcceleration          = '409A6000'
writeHomingAcceleraiton         = '239A6000'
#60C2 interpolation time period
readInterpolationTimePeriodValue    = '40C26001'
writeInterpolationTimePeriodValue   = '2FC26001'
readInterpolationTimePeriodIndex    = '40C26002'
writeInterpolationTimePeriodIndex   = '2FC26002'
#60C5 max acceleration
readMaxAcceleration         = '40C56000'
writeMaxAcceleration        = '23C56000'
#60C6 max deceleration
readMaxDeceleration         = '40C66000'
writeMaxDeceleration        = '23C66000'
#60FF target velocity
readTargetVelocity          = '40FF6000'
writeTargetVelocity         = '23FF6000'


referrenceList = ['none',
                  '603F_errorCode',
                  '6040_controlWord',
                  '6041_statusWord',
                  '6060_mode',
                  '6061_modeOfOperationDisplay',
                  '6062_positionDemandValue',
                  '6064_positionActualValue',
                  '6065_followingErrorWindow',
                  '6066_followingErrorTimeout',
                  '6067_positionWindow',
                  '6068_positionWindowTime',
                  '606B_velocityDemandValue',
                  '606C_velocityActualValue',
                  '606D_velocityWindow',
                  '606E_velocityWindowTime',
                  '606F_velocityThreshold',
                  '6070_velocityThresholdTime',
                  '6071_targetTorque',
                  '6072_maxTorque',
                  '6074_torqueDemand',
                  '6075_motorRatedCurrent',
                  '6077_torqueActualValue',
                  '6079_dclinkCircuitVoltage',
                  '607A_targetPosition',
                  '607E_polarity',
                  '607F_maxProfileVelocity',
                  '6080_maxMotorSpeed',
                  '6081_profileVelocity',
                  '6083_profileAcceleration',
                  '6084_profileDeceleration',
                  '6085_quickstopDeceleration',
                  '6087_torqueSlope',
                  '60B0_positionOffset',
                  '60B1_velocityOffset',
                  '60B2_torqueOffset',
                  '60C5_maxAcceleration',
                  '60C6_maxDeceleration',
                  '60F2_positionOptionCode',
                  '60F4_followingerrorActualValue',
                  '60FF_targetVelocity',
                  '6502_supportedDriveModes']

tpdoAvailableList = ['none',
                     '2017_iitValue',
                     '201B_temperature',
                     '2240_digitalInputValue',
                     '2250_digitalOutputValue',
                     '3000_absTargetPosition',   
                     '3100_nlsPosition',
                     '3101_plsPosition',
                     '603F_errorCode',
                     '6041_statusWord',
                     '6061_modeOfOperationDisplay',
                     '6062_positionDemandValue',
                     '6064_positionActualValue',
                     '606B_velocityDemandValue',
                     '606C_velocityActualValue',
                     '6071_targetTorque',
                     '6074_torqueDemand',
                     '6077_torqueActualValue',
                     '6079_dclinkCircuitVoltage',
                     '607A_targetPosition',
                     '6081_profileVelocity',
                     '60C1_interpolationDataRecord',
                     '60F4_followingerrorActualValue',
                     '60FD_digitalInputs',
                     '60FF_targetVelocity']

rpdoAvailableList = ['none',
                     '6040_controlWord',
                     '6060_mode',
                     '6065_followingErrorWindow',
                     '6066_followingErrorTimeout',
                     '6067_positionWindow',
                     '6068_positionWindowTime',
                     '606D_velocityWindow',
                     '606E_velocityWindowTime',
                     '606F_velocityThreshold',
                     '6070_velocityThresholdTime',
                     '6071_targetTorque',
                     '6072_maxTorque',
                     '607A_targetPosition',
                     '607C_homeOffset',
                     '607E_polarity',
                     '607F_maxProfileVelocity',
                     '6081_profileVelocity',
                     '6083_profileAcceleration',
                     '6084_profileDeceleration',
                     '6085_quickstopDeceleration',
                     '6087_torqueSlope',
                     '609A_homingAcceleration',
                     '60B0_positionOffset',
                     '60B1_velocityOffset',
                     '60B2_torqueOffset',
                     '60C1_interpolationDataRecord',
                     '60C5_maxAcceleration',
                     '60C6_maxDeceleration',
                     '60FE_digitalOutputs',
                     '60FF_targetVelocity']
listOfNodeid = [  '1','2','3','4','5','6','7','8','9','10',
                  '11','12','13','14','15','16','17','18','19','20', 
                  '21','22','23','24','25','26','27','28','29','30', 
                  '31','32','33','34','35','36','37','38','39','40',   
                  '41','42','43','44','45','46','47','48','49','50',   
                  '51','52','53','54','55','56','57','58','59','60',   
                  '61','62','63','64','65','66','67','68','69','70',   
                  '71','72','73','74','75','76','77','78','79','80',  
                  '81','82','83','84','85','86','87','88','89','90',  
                  '91','92','93','94','95','96','97','98','99','100', 
                  '101','102','103','104','105','106','107','108','109','110',
                  '111','112','113','114','115','116','117','118','119','120',
                  '121','122','123','124','125','126','127']
                  
listOfTpdoTransmissionType = ['0','1','2','3','4','5','6','7','8','9','10',
                              '11','12','13','14','15','16','17','18','19','20', 
                              '21','22','23','24','25','26','27','28','29','30', 
                              '31','32','33','34','35','36','37','38','39','40',   
                              '41','42','43','44','45','46','47','48','49','50',   
                              '51','52','53','54','55','56','57','58','59','60',   
                              '61','62','63','64','65','66','67','68','69','70',   
                              '71','72','73','74','75','76','77','78','79','80',  
                              '81','82','83','84','85','86','87','88','89','90',  
                              '91','92','93','94','95','96','97','98','99','100', 
                              '101','102','103','104','105','106','107','108','109','110',
                              '111','112','113','114','115','116','117','118','119','120',
                              '121','122','123','124','125','126','127','128','129','130',
                              '131','132','133','134','135','136','137','138','139','140', 
                              '141','142','143','144','145','146','147','148','149','150', 
                              '151','152','153','154','155','156','157','158','159','160', 
                              '161','162','163','164','165','166','167','168','169','170',   
                              '171','172','173','174','175','176','177','178','179','180',  
                              '181','182','183','184','185','186','187','188','189','190',  
                              '191','192','193','194','195','196','197','198','199','200', 
                              '201','202','203','204','205','206','207','208','209','210',
                              '211','212','213','214','215','216','217','218','219','220',
                              '221','222','223','224','225','226','227','228','229','230',
                              '231','232','233','234','235','236','237','238','239','252','253','254','255']
listOfRpdoTransmissionType = ['0','1','2','3','4','5','6','7','8','9','10',
                              '11','12','13','14','15','16','17','18','19','20', 
                              '21','22','23','24','25','26','27','28','29','30', 
                              '31','32','33','34','35','36','37','38','39','40',   
                              '41','42','43','44','45','46','47','48','49','50',   
                              '51','52','53','54','55','56','57','58','59','60',   
                              '61','62','63','64','65','66','67','68','69','70',   
                              '71','72','73','74','75','76','77','78','79','80',  
                              '81','82','83','84','85','86','87','88','89','90',  
                              '91','92','93','94','95','96','97','98','99','100', 
                              '101','102','103','104','105','106','107','108','109','110',
                              '111','112','113','114','115','116','117','118','119','120',
                              '121','122','123','124','125','126','127','128','129','130',
                              '131','132','133','134','135','136','137','138','139','140', 
                              '141','142','143','144','145','146','147','148','149','150', 
                              '151','152','153','154','155','156','157','158','159','160', 
                              '161','162','163','164','165','166','167','168','169','170',   
                              '171','172','173','174','175','176','177','178','179','180',  
                              '181','182','183','184','185','186','187','188','189','190',  
                              '191','192','193','194','195','196','197','198','199','200', 
                              '201','202','203','204','205','206','207','208','209','210',
                              '211','212','213','214','215','216','217','218','219','220',
                              '221','222','223','224','225','226','227','228','229','230',
                              '231','232','233','234','235','236','237','238','239','254','255']
listOfTpdoSyncStartValue    = ['0','1','2','3','4','5','6','7','8','9','10',
                              '11','12','13','14','15','16','17','18','19','20', 
                              '21','22','23','24','25','26','27','28','29','30', 
                              '31','32','33','34','35','36','37','38','39','40',   
                              '41','42','43','44','45','46','47','48','49','50',   
                              '51','52','53','54','55','56','57','58','59','60',   
                              '61','62','63','64','65','66','67','68','69','70',   
                              '71','72','73','74','75','76','77','78','79','80',  
                              '81','82','83','84','85','86','87','88','89','90',  
                              '91','92','93','94','95','96','97','98','99','100', 
                              '101','102','103','104','105','106','107','108','109','110',
                              '111','112','113','114','115','116','117','118','119','120',
                              '121','122','123','124','125','126','127','128','129','130',
                              '131','132','133','134','135','136','137','138','139','140', 
                              '141','142','143','144','145','146','147','148','149','150', 
                              '151','152','153','154','155','156','157','158','159','160', 
                              '161','162','163','164','165','166','167','168','169','170',   
                              '171','172','173','174','175','176','177','178','179','180',  
                              '181','182','183','184','185','186','187','188','189','190',  
                              '191','192','193','194','195','196','197','198','199','200', 
                              '201','202','203','204','205','206','207','208','209','210',
                              '211','212','213','214','215','216','217','218','219','220',
                              '221','222','223','224','225','226','227','228','229','230',
                              '231','232','233','234','235','236','237','238','239']
ojbectDict = { 
               '2017_iitValue':                  ['20170220','4'],
               '201B_temperature':               ['201B0120','4'],
               '2240_digitalInputValue':         ['22400320','4'],
               '2250_digitalOutputValue':        ['22500320','4'],
               '3000_absTargetPosition':         ['30000020','4'],
               '3100_nlsPosition':               ['31000020','4'],
               '3101_plsPosition':               ['31010020','4'],
               '603F_errorCode':                 ['603F0010','2'],
               '6040_controlWord':               ['60400010','2'], 
               '6041_statusWord':                ['60410010','2'],
               '6060_mode':                      ['60600008','1'],
               '6061_modeOfOperationDisplay':    ['60610008','1'],
               '6062_positionDemandValue':       ['60620020','4'],
               '6064_positionActualValue':       ['60640020','4'],
               '6065_followingErrorWindow':      ['60650020','4'],
               '6066_followingErrorTimeout':     ['60660010','2'],
               '6067_positionWindow':            ['60670020','4'],
               '6068_positionWindowTime':        ['60680010','2'],
               '606B_velocityDemandValue':       ['606B0020','4'],
               '606C_velocityActualValue':       ['606C0020','4'],
               '606D_velocityWindow':            ['606D0010','2'],
               '606E_velocityWindowTime':        ['606E0010','2'],
               '606F_velocityThreshold':         ['606F0010','2'],
               '6070_velocityThresholdTime':     ['60700010','2'],
               '6071_targetTorque':              ['60710010','2'],
               '6072_maxTorque':                 ['60720010','2'],
               '6074_torqueDemand':              ['60740010','2'],
               '6077_torqueActualValue':         ['60770010','2'],
               '6079_dclinkCircuitVoltage':      ['60790020','4'],
               '607A_targetPosition':            ['607A0020','4'],
               '607C_homeOffset':                ['607C0020','4'],
               '607E_polarity':                  ['607E0008','1'],
               '607F_maxProfileVelocity':        ['607F0020','4'],
               '6081_profileVelocity':           ['60810020','4'],
               '6083_profileAcceleration':       ['60830020','4'],
               '6084_profileDeceleration':       ['60840020','4'],
               '6085_quickstopDeceleration':     ['60850020','4'],
               '6087_torqueSlope':               ['60870020','4'],
               '609A_homingAcceleration':        ['609A0020','4'],
               '60B0_positionOffset':            ['60B00020','4'],
               '60B1_velocityOffset':            ['60B10020','4'],
               '60B2_torqueOffset':              ['60B20010','2'],
               '60C1_interpolationDataRecord':   ['60C10120','4'],
               '60C5_maxAcceleration':           ['60C50020','4'],
               '60C6_maxDeceleration':           ['60C60020','4'],
               '60F2_positionOptionCode':        ['60F20010','2'],
               '60F4_followingerrorActualValue': ['60F40020','4'],
               '60FD_digitalInputs':             ['60FD0020','4'],
               '60FF_targetVelocity':            ['60FF0020','4'],                        
              }  
listOfHomingMethod = [  '1','2','3','4','5','6','7','8','9','10',
                        '11','12','13','14','17','18','19','20', 
                        '21','22','23','24','25','26','27','28','29','30', 
                        '33','34','35',  
                        '-1','-2','-7','-8','-9','-10',
                        '-11','-12','-13','-14','-17','-18',
                        '-23','-24','-25','-26','-27','-28','-29','-30']
homingMethodDict = {'1':        0,
                    '2':        1, 
                    '3':        2, 
                    '4':        3, 
                    '5':        4, 
                    '6':        5, 
                    '7':        6, 
                    '8':        7,
                    '9':        8,
                    '10':       9,
                    '11':       10,
                    '12':       11, 
                    '13':       12, 
                    '14':       13, 
                    '17':       14, 
                    '18':       15,
                    '19':       16,
                    '20':       17,
                    '21':       18,
                    '22':       19, 
                    '23':       20, 
                    '24':       21, 
                    '25':       22, 
                    '26':       23, 
                    '27':       24, 
                    '28':       25,
                    '29':       26,
                    '30':       27,
                    '33':       28, 
                    '34':       29, 
                    '35':       30, 
                    '-1':       31,
                    '-2':       32, 
                    '-7':       33, 
                    '-8':       34,
                    '-9':       35,
                    '-10':      36,
                    '-11':      37,
                    '-12':      38, 
                    '-13':      39, 
                    '-14':      40, 
                    '-17':      41, 
                    '-18':      42,
                    '-23':      43, 
                    '-24':      44, 
                    '-25':      45, 
                    '-26':      46, 
                    '-27':      47, 
                    '-28':      48,
                    '-29':      49,
                    '-30':      50,
              } 
crctable = [ 
            0x0000, 0x1021, 0x2042, 0x3063, 0x4084, 0x50A5, 0x60C6, 0x70E7, 0x8108, 0x9129, 0xA14A, 0xB16B, 0xC18C, 0xD1AD, 0xE1CE, 0xF1EF,
            0x1231, 0x0210, 0x3273, 0x2252, 0x52B5, 0x4294, 0x72F7, 0x62D6, 0x9339, 0x8318, 0xB37B, 0xA35A, 0xD3BD, 0xC39C, 0xF3FF, 0xE3DE,
            0x2462, 0x3443, 0x0420, 0x1401, 0x64E6, 0x74C7, 0x44A4, 0x5485, 0xA56A, 0xB54B, 0x8528, 0x9509, 0xE5EE, 0xF5CF, 0xC5AC, 0xD58D,
            0x3653, 0x2672, 0x1611, 0x0630, 0x76D7, 0x66F6, 0x5695, 0x46B4, 0xB75B, 0xA77A, 0x9719, 0x8738, 0xF7DF, 0xE7FE, 0xD79D, 0xC7BC,
            0x48C4, 0x58E5, 0x6886, 0x78A7, 0x0840, 0x1861, 0x2802, 0x3823, 0xC9CC, 0xD9ED, 0xE98E, 0xF9AF, 0x8948, 0x9969, 0xA90A, 0xB92B,
            0x5AF5, 0x4AD4, 0x7AB7, 0x6A96, 0x1A71, 0x0A50, 0x3A33, 0x2A12, 0xDBFD, 0xCBDC, 0xFBBF, 0xEB9E, 0x9B79, 0x8B58, 0xBB3B, 0xAB1A,
            0x6CA6, 0x7C87, 0x4CE4, 0x5CC5, 0x2C22, 0x3C03, 0x0C60, 0x1C41, 0xEDAE, 0xFD8F, 0xCDEC, 0xDDCD, 0xAD2A, 0xBD0B, 0x8D68, 0x9D49,
            0x7E97, 0x6EB6, 0x5ED5, 0x4EF4, 0x3E13, 0x2E32, 0x1E51, 0x0E70, 0xFF9F, 0xEFBE, 0xDFDD, 0xCFFC, 0xBF1B, 0xAF3A, 0x9F59, 0x8F78,
            0x9188, 0x81A9, 0xB1CA, 0xA1EB, 0xD10C, 0xC12D, 0xF14E, 0xE16F, 0x1080, 0x00A1, 0x30C2, 0x20E3, 0x5004, 0x4025, 0x7046, 0x6067,
            0x83B9, 0x9398, 0xA3FB, 0xB3DA, 0xC33D, 0xD31C, 0xE37F, 0xF35E, 0x02B1, 0x1290, 0x22F3, 0x32D2, 0x4235, 0x5214, 0x6277, 0x7256,
            0xB5EA, 0xA5CB, 0x95A8, 0x8589, 0xF56E, 0xE54F, 0xD52C, 0xC50D, 0x34E2, 0x24C3, 0x14A0, 0x0481, 0x7466, 0x6447, 0x5424, 0x4405,
            0xA7DB, 0xB7FA, 0x8799, 0x97B8, 0xE75F, 0xF77E, 0xC71D, 0xD73C, 0x26D3, 0x36F2, 0x0691, 0x16B0, 0x6657, 0x7676, 0x4615, 0x5634,
            0xD94C, 0xC96D, 0xF90E, 0xE92F, 0x99C8, 0x89E9, 0xB98A, 0xA9AB, 0x5844, 0x4865, 0x7806, 0x6827, 0x18C0, 0x08E1, 0x3882, 0x28A3,
            0xCB7D, 0xDB5C, 0xEB3F, 0xFB1E, 0x8BF9, 0x9BD8, 0xABBB, 0xBB9A, 0x4A75, 0x5A54, 0x6A37, 0x7A16, 0x0AF1, 0x1AD0, 0x2AB3, 0x3A92,
            0xFD2E, 0xED0F, 0xDD6C, 0xCD4D, 0xBDAA, 0xAD8B, 0x9DE8, 0x8DC9, 0x7C26, 0x6C07, 0x5C64, 0x4C45, 0x3CA2, 0x2C83, 0x1CE0, 0x0CC1,
            0xEF1F, 0xFF3E, 0xCF5D, 0xDF7C, 0xAF9B, 0xBFBA, 0x8FD9, 0x9FF8, 0x6E17, 0x7E36, 0x4E55, 0x5E74, 0x2E93, 0x3EB2, 0x0ED1, 0x1EF0]
#description: name, index, subindex, length, isValid, data   
eepromListSubindexOfName = 0
eepromListSubindexOfIndex = 1
eepromListSubindexOfSubindex = 2
eepromListSubindexOfLen = 3
eepromListSubindexOfSign = 4
eepromListSubindexOfValid = 5
eepromListSubindexOfData = 6
eepromList = [    ['200101_nodeid',                         '2001','01',1,False,'False',0], 
                  ['200102_canBitRate',                     '2001','02',2,False,'False',0],    
                  ['200102_en120Resistor',                  '2001','03',1,False,'False',0], 
                  ['200301_conterPerResolution',            '2003','01',4,False,'False',0], 
                  ['201003_currentKp',                      '2010','03',4,False,'False',0],
                  ['201004_currentKi',                      '2010','04',4,False,'False',0],
                  ['201005_currentBandwitdh',               '2010','05',4,False,'False',0],
                  ['201203_velocityKp',                     '2012','03',4,False,'False',0],
                  ['201204_velocityKi',                     '2012','04',4,False,'False',0],
                  ['201205_velocityStiffness',              '2012','05',4,False,'False',0],
                  ['201302_positionKp',                     '2013','02',4,False,'False',0],
                  ['201404_autoBrake',                      '2014','04',1,False,'False',0],
                  ['201501_cspDoInterpolation',             '2015','01',1,False,'False',0],
                  ['201502_csvDoInterpolation',             '2015','02',1,False,'False',0],
                  ['201503_cstDoInterpolation',             '2015','03',1,False,'False',0],
                  ['201504_torqueWithPosition',             '2015','04',1,False,'False',0],
                  ['201505_stepdirWithoutCanopen',          '2015','05',1,False,'False',0],
                  ['201601_velocityFilterBw',               '2016','01',4,False,'False',0],
                  ['201602_accelFilterBw',                  '2016','02',4,False,'False',0],
                  ['201603_iitFilterBw',                    '2016','03',4,False,'False',0],
                  ['201605_temperatureFilterBw',            '2016','05',4,False,'False',0],
                  ['201607_brakeCurrentFilterBw',           '2016','07',4,False,'False',0],
                  ['201608_inputPositionFilterBw',          '2016','08',4,False,'False',0],
                  ['201701_iitLimit',                       '2017','01',4,False,'False',0],
                  ['201703_iitOnThreshold',                 '2017','03',4,False,'False',0],
                  ['201801_overVoltageThreshold',           '2018','01',4,False,'False',0],
                  ['201802_underVoltageThreshold',          '2018','02',4,False,'False',0],
                  ['201901_emcyEnVelocityLost',             '2019','01',1,False,'False',0],
                  ['201902_emcyEnIit',                      '2019','02',1,False,'False',0],
                  ['201903_emcyEnHbLost',                   '2019','03',1,False,'False',0],
                  ['201904_emcyEnSyncTimeOut',              '2019','04',1,False,'False',0],
                  ['201905_emcyEnRxOverrun',                '2019','05',1,False,'False',0],
                  ['201906_emcyEnTxOverrun',                '2019','06',1,False,'False',0],
                  ['201907_emcyEnRemotereset',              '2019','07',1,False,'False',0],
                  ['201908_emcyEnTpdoOutWindow',            '2019','08',1,False,'False',0],
                  ['201909_emcyEnRpdolength',               '2019','09',1,False,'False',0],
                  ['20190A_emcyEnRpdoTimeout',              '2019','0A',1,False,'False',0],
                  ['20190B_emcyEnSyncDatalength',           '2019','0B',1,False,'False',0],
                  ['201A01_velocityFeedforward',            '201A','01',2,False,'False',0],
                  ['201A02_accelFeedforward',               '201A','02',2,False,'False',0],
                  ['201B03_maxBoardTempereature',           '201B','03',4,False,'False',0],
                  ['201B04_minBoardTempereature',           '201B','04',4,True ,'False',0],
                  ['201B05_maxMotorTempereature',           '201B','05',4,False,'False',0],
                  ['201B06_minMotorTempereature',           '201B','06',4,True ,'False',0],
                  ['201C01_resistorValue',                  '201C','01',4,False,'False',0],
                  ['201C02_resistorStartVoltage',           '201C','02',4,False,'False',0],
                  ['201C03_resistorStopVoltage',            '201C','03',4,False,'False',0],
                  ['203000_torqueWindow',                   '2030','00',2,False,'False',0],
                  ['203100_torqueWindowTimeout',            '2031','00',2,False,'False',0],
                  ['203300_syncIntime',                     '2033','00',2,False,'False',0],
                  ['203400_internalTargetReachWindow',      '2034','00',2,False,'False',0],
                  ['203A01_blockTriggerCurrent',            '203A','01',4,True ,'False',0],
                  ['203A02_blockDuration',                  '203A','02',2,False,'False',0],
                  ['203B01_limitSwitchType',                '203B','01',4,False,'False',0],
                  ['224001_digitalInputFunctionEnable',     '2240','01',4,False,'False',0],
                  ['224002_digitalInputInverted',           '2240','02',4,False,'False',0],
                  ['225001_digitalOutputFunctionEnable',    '2250','01',4,False,'False',0],
                  ['225002_digitalOutputInverted',          '2250','02',4,False,'False',0],
                  ['606500_followingErrorWindow',           '6065','00',4,False,'False',0],
                  ['606600_followingErrorTimeout',          '6066','00',2,False,'False',0],
                  ['606700_positionWindow',                 '6067','00',4,False,'False',0],
                  ['606800_positionWindowTime',             '6068','00',2,False,'False',0],
                  ['606D00_velocityWindow',                 '606D','00',2,False,'False',0],
                  ['606E00_velocityWindowTime',             '606E','00',2,False,'False',0],
                  ['606F00_velocityThreshold',              '606F','00',2,False,'False',0],
                  ['607000_velocityThresholdTime',          '6070','00',2,False,'False',0],
                  ['607200_maxTorque',                      '6072','00',2,False,'False',0],
                  ['607C00_homeOffset',                     '607C','00',4,False,'False',0],
                  ['607D01_softwarePositionLimitP',         '607D','01',4,True ,'False',0],
                  ['607D02_softwarePositionLimitN',         '607D','02',4,True ,'False',0],
                  ['607E00_polarity',                       '607E','00',1,False,'False',0],
                  ['607F00_maxProfileVelocity',             '607F','00',4,False,'False',0],
                  ['608300_profileAcceleration',            '6083','00',4,False,'False',0],
                  ['608400_profileDeceleration',            '6084','00',4,False,'False',0],
                  ['608500_quickstopDeceleration',          '6085','00',4,False,'False',0],
                  ['608700_torqueSlope',                    '6087','00',4,False,'False',0],
                  ['609301_positionNumerator',              '6093','01',4,False,'False',0],
                  ['609302_positionDivisor',                '6093','02',4,False,'False',0],
                  ['609501_velocityNumerator',              '6095','01',4,False,'False',0],
                  ['609502_velocityDivisor',                '6095','02',4,False,'False',0],
                  ['609701_accelNumerator',                 '6097','01',4,False,'False',0],
                  ['609702_accelDivisor',                   '6097','02',4,False,'False',0],
                  ['609800_homingMethod',                   '6098','00',1,False,'False',0],
                  ['609901_homingSpeeds1',                  '6099','01',4,False,'False',0],
                  ['609902_homingSpeeds2',                  '6099','02',4,False,'False',0],
                  ['609A00_homingAccel',                    '609A','00',4,False,'False',0],
                  ['60C500_maxAcceleration',                '60C5','00',4,False,'False',0],
                  ['60C600_maxDeceleration',                '60C6','00',4,False,'False',0]                       
              ]