import xml.etree.ElementTree as ET


class DrawioRenderer:


    def cell(
        self,
        root,
        cid,
        value,
        style,
        vertex=False,
        edge=False
    ):

        attr = {

            "id": cid,

            "value": value,

            "style": style,

            "parent": "1"

        }


        if vertex:

            attr["vertex"] = "1"


        if edge:

            attr["edge"] = "1"



        return ET.SubElement(

            root,

            "mxCell",

            attr

        )




    def geo(
        self,
        cell,
        x,
        y,
        w,
        h
    ):


        ET.SubElement(

            cell,

            "mxGeometry",

            {

                "x": str(x),

                "y": str(y),

                "width": str(w),

                "height": str(h),

                "as": "geometry"

            }

        )





    def render(
        self,
        data,
        layout,
        output
    ):


        mxfile = ET.Element(
            "mxfile"
        )


        diagram = ET.SubElement(
            mxfile,
            "diagram"
        )


        model = ET.SubElement(
            diagram,
            "mxGraphModel"
        )


        root = ET.SubElement(
            model,
            "root"
        )



        ET.SubElement(
            root,
            "mxCell",
            {
                "id":"0"
            }
        )


        ET.SubElement(
            root,
            "mxCell",
            {
                "id":"1",
                "parent":"0"
            }
        )



        # ==========================
        # 根据节点位置动态计算泳道高度
        # ==========================

        lane_height = 800


        for pos in layout.values():

            lane_height = max(

                lane_height,

                pos["y"]

            )


        # 给底部留空间

        lane_height += 200





        # ==========================
        # 泳道
        # ==========================

        for i,lane in enumerate(data["lanes"]):


            c = self.cell(

                root,

                "lane_" + lane["id"],

                lane["name"],

                "swimlane;horizontal=1;startSize=40",

                True

            )


            self.geo(

                c,

                i * 260,

                0,

                260,

                lane_height

            )





        # ==========================
        # 节点样式
        # ==========================

        styles = {


            "start":

            "ellipse",



            "end":

            "ellipse",



            "process":

            "rounded=1",



            "decision":

            "rhombus",



            "document":

            "shape=document",



            "database":

            "shape=cylinder",



            "human":

            "shape=mxgraph.basic.user",



            "input":

            "shape=parallelogram",



            "output":

            "shape=mxgraph.basic.exit",



            "api":

            "shape=hexagon",



            "subprocess":

            "rounded=1;double=1"

        }





        # ==========================
        # 节点
        # ==========================

        for n in data["nodes"]:


            style = styles.get(

                n["type"],

                "rounded=1"

            )


            c = self.cell(

                root,

                n["id"],

                n["text"],

                style,

                vertex=True

            )


            self.geo(

                c,

                layout[n["id"]]["x"],

                layout[n["id"]]["y"],

                140,

                60

            )






        # ==========================
        # 连线
        # ==========================

        for e in data["edges"]:


            c = self.cell(

                root,

                "edge_"

                +

                e["source"]

                +

                "_"

                +

                e["target"],


                e.get(
                    "label",
                    ""
                ),


                (
                    "edgeStyle=orthogonalEdgeStyle;"
                    "rounded=1;"
                    "orthogonalLoop=1;"
                    "jettySize=auto;"
                    "endArrow=classic"
                ),


                edge=True

            )



            c.set(

                "source",

                e["source"]

            )


            c.set(

                "target",

                e["target"]

            )



            ET.SubElement(

                c,

                "mxGeometry",

                {

                    "relative":"1",

                    "as":"geometry"

                }

            )





        ET.ElementTree(

            mxfile

        ).write(

            output,

            encoding="utf-8",

            xml_declaration=True

        )