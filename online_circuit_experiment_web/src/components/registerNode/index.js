// svg png 图片资源来自阿里字体库
// [阿里字体库](https://www.iconfont.cn/collections/index?spm=a313x.7781069.1998910419.4)
// svg图标建议使用自己创建的
import registerStart from '@/components/registerNode/registerStart.js'
import registerUser from "@/components/registerNode/registerUser";
import registerEnd from './registerEnd'
import registerPush from './registerPush'
import registerDownload from './registerDownload'
import registerPolyline from './registerPolyline'
import registerBezier from "@/components/registerNode/registerBezier";
import registerTask from './registerTask'
import registerConnect from './registerConnect'
import registerMultimeteRealrNode from "@/components/registerNode/registerMultimeterRealNode";
import registerSignalGeneratorRealNode from "@/components/registerNode/registerSignalGeneratorRealNode";
import registerDCPowerSupplyRealNode from "@/components/registerNode/registerDCPowerSupplyRealNode";
import registerResistanceBoxNode from "@/components/registerNode/registerResistanceBoxNode";
import registerCapacitanceBoxNode from "@/components/registerNode/registerCapacitanceBoxNode";
import registerInductanceBoxNode from "@/components/registerNode/registerInductanceBoxNode";
import registerOscilloscopeRealNode from '@/components/registerNode/registerOscilloscope'

import registerInductanceRealNode from "@/components/registerNode/registerInductanceRealNode";
import registerResistanceRealNode from "@/components/registerNode/registerResistanceRealNode";
import registerCapacitanceRealNode from "@/components/registerNode/registerCapacitanceRealNode";
import registerDiodeRealNode from "@/components/registerNode/registerDiodeRealNode";
import registerMOSFETRealNode from "@/components/registerNode/registerMOSFETRealNode";
import registerGNDNode from '@/components/registerNode/registerGNDNode'
import register8720DMNode from "@/components/registerNode/register8720DMNode";
// 感觉应该将
export const registerCustomNode = (lf) => {
    registerStart(lf)
    registerUser(lf)
    registerEnd(lf)
    registerPush(lf)
    registerDownload(lf)
    registerPolyline(lf)
    registerBezier(lf)
    registerTask(lf)
    registerConnect(lf)



    registerMultimeteRealrNode(lf)
    registerSignalGeneratorRealNode(lf)
    registerDCPowerSupplyRealNode(lf)
    registerResistanceBoxNode(lf)
    registerCapacitanceBoxNode(lf)
    registerInductanceBoxNode(lf)
    registerOscilloscopeRealNode(lf)

    registerResistanceRealNode(lf)
    registerInductanceRealNode(lf)
    registerCapacitanceRealNode(lf)
    registerDiodeRealNode(lf)
    registerMOSFETRealNode(lf)
    registerGNDNode(lf)
    register8720DMNode(lf)
}
