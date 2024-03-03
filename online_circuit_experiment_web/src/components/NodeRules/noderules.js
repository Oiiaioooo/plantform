// 每一个节点的文件都导入这个
// 规则：
// 1.将等效的节点视为同一类节点，例如在实验里，将各种仪器
// 的负极和地都是为地，因为都是连在一起的。所以当某种节点和地类型节点连接时，后端都视为与地相连
// 2.预先定义好的连线不能被操作
// 3.每次连线的时候都看看有没有重复连线，即拿到所有连线，看看是不是已经有sourceanchor和targetanchor一样的连线，有了就不连了
// 4.每次连线检查是不是允许的链接，实现定义了表格，哪几类等效节点可以连接。（节点都视为等效节点，连接关系也是）
// const demoData = require('./data_circuit.json')

import {Message} from "element-ui";

let circuit_nodes = 23;

function generate_matrix(n) {
    let matrix = Array.from(Array(n), () => new Array(n).fill(0));
    let count = 1;
    for (let i = 0; i < n; i++) {
        for (let j = i + 1; j < n; j++) {
            matrix[i][j] = count;
            matrix[j][i] = count;
            count += 1;
        }
    }
    return matrix;
}

let connectMatrix = generate_matrix(circuit_nodes);


export const circuitRules = function () {
    const circuitNodeAnchorType = JSON.parse(sessionStorage.getItem('cnodeAnchor') || '{}');
    return [
        //禁止重复连线,不过其实没必要禁止重复连线，因为没有什么影响
        // ...

        //矩阵连线规则
        {
            message: "不支持的连线",
            validate: (sourceNode, targetNode, sourceAnchor, targetAnchor) => {
                // console.log(sourceNode, targetNode, sourceAnchor, targetAnchor)

                let sourceAnchorTypeIndex = -1
                // 对sourceAnchor进行遍历，找到其属于哪一类nodeType, key 代表的是anchor的类型，即电路节点号
                for (const key in circuitNodeAnchorType) {
                    // 遍历锚点是否是在某一个节点对应的数组内
                    const sourceIndex = circuitNodeAnchorType[key].indexOf(sourceAnchor.id)
                    // 若index>-1则说明sourceAnchor存在
                    if (sourceIndex > -1) {
                        // 源锚点的节点类型
                        sourceAnchorTypeIndex = Object.keys(circuitNodeAnchorType).indexOf(key)
                        break
                    }
                }
                // console.log('sourceAnchorTypeIndex', sourceAnchorTypeIndex)

                let targetAnchorTypeIndex = -1
                // 对targetAnchor进行遍历，找到其属于哪一类nodeType
                for (const key in circuitNodeAnchorType) {
                    // 遍历锚点是否是在某一个节点的数组内
                    const targetIndex = circuitNodeAnchorType[key].indexOf(targetAnchor.id)
                    // 若index>-1则说明存在
                    if (targetIndex > -1) {
                        // 源锚点的节点类型
                        targetAnchorTypeIndex = Object.keys(circuitNodeAnchorType).indexOf(key)
                        break
                    }
                }
                // console.log('targetAnchorTypeIndex', targetAnchorTypeIndex)
                // 即在上一个循环中发现不属于任何一类，则为不可连线的类型
                if (sourceAnchorTypeIndex === -1) {
                    // Message({
                    //     message: "源锚点不可连接",
                    //     type: 'error',
                    //     duration: 3 * 1000
                    // })
                    return false
                } else if (targetAnchorTypeIndex === -1) {
                    // Message({
                    //     message: "目标锚点不可连接",
                    //     type: 'error',
                    //     duration: 3 * 1000
                    // })
                    return false
                }
                // 否则说明是sourceAnchorType类的节点，具有可连接性，根据这个可以找到其所有可以进行连接的点。
                else {
                    // source和target对应的节点类型的连线，其在矩阵中的值
                    const value = connectMatrix[sourceAnchorTypeIndex][targetAnchorTypeIndex]
                    // 转置后的值
                    const value_T = connectMatrix[targetAnchorTypeIndex][sourceAnchorTypeIndex]
                    // 矩阵中对应的索引，如果存在值不为0，说明可连接
                    if (value > 0 || value_T > 0) {
                        // const valueMatrix = value_T > 0 ? value_T : value
                        // Message({
                        //     message:"合法连接",
                        //     type:'success',
                        //     duration:3*1000
                        // })
                        // 注意不能在校验这里向后端传值，因为校验会频繁触发
                        // console.log(valueMatrix)
                        return true
                    } else {
                        Message({
                            message: "不支持的连线",
                            type: 'error',
                            duration: 3 * 1000
                        })
                        return false
                    }
                }
            }
        }
    ]
}
