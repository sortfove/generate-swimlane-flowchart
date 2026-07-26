from collections import defaultdict, deque



class LayoutEngine:


    def __init__(self):

        # 泳道宽度
        self.lane_width = 260


        # 节点尺寸

        self.node_width = 140

        self.node_height = 60


        # 层级间距

        self.level_height = 130


        # 同泳道同层节点纵向偏移

        self.same_level_offset = 90





    # ==========================
    # 构建流程图关系
    # ==========================

    def build_graph(
            self,
            data
    ):


        graph = defaultdict(list)

        indegree = defaultdict(int)



        for edge in data["edges"]:


            graph[
                edge["source"]
            ].append(
                edge["target"]
            )



            indegree[
                edge["target"]
            ] += 1



        return graph, indegree






    # ==========================
    # 拓扑排序计算层级
    # ==========================

    def calculate_level(
            self,
            data
    ):


        graph, indegree = self.build_graph(
            data
        )



        level = {}

        queue = deque()



        # 找入口节点

        for node in data["nodes"]:


            if indegree[node["id"]] == 0:


                queue.append(
                    node["id"]
                )


                level[
                    node["id"]
                ] = 0





        while queue:


            current = queue.popleft()



            for nxt in graph[current]:


                level[nxt] = max(

                    level.get(
                        nxt,
                        0
                    ),

                    level[current] + 1

                )



                indegree[nxt] -= 1



                if indegree[nxt] == 0:


                    queue.append(
                        nxt
                    )



        return level







    # ==========================
    # 跨泳道水平对齐
    #
    # 左 -> 右
    #
    # 右 -> 左
    #
    # 支持:
    # process
    # database
    # api
    # document
    # human
    #
    # 不处理:
    # start
    # end
    # decision
    # subprocess
    # ==========================

    def align_cross_lane(
            self,
            data,
            level
    ):



        node_map = {

            node["id"]: node

            for node in data["nodes"]

        }




        lane_index = {}



        for i,lane in enumerate(data["lanes"]):


            lane_index[
                lane["id"]
            ] = i





        # 可参与普通对齐节点

        normal_types = [

            "process",

            "database",

            "api",

            "document",

            "human",

            "input",

            "output"

        ]



        # 不参与对齐节点

        special_types = [

            "start",

            "end",

            "decision",

            "subprocess"

        ]





        for edge in data["edges"]:



            source = node_map[
                edge["source"]
            ]


            target = node_map[
                edge["target"]
            ]




            source_lane = lane_index[
                source["lane"]
            ]



            target_lane = lane_index[
                target["lane"]
            ]




            # 只处理相邻泳道

            if abs(
                source_lane-target_lane
            ) != 1:


                continue





            # 特殊节点跳过

            if source["type"] in special_types:


                continue



            if target["type"] in special_types:


                continue





            if (

                source["type"] in normal_types

                and

                target["type"] in normal_types

            ):




                # ----------------------
                # 左 -> 右
                # ----------------------

                if source_lane < target_lane:


                    level[
                        target["id"]
                    ] = level[
                        source["id"]
                    ]





                # ----------------------
                # 右 -> 左
                # ----------------------

                elif source_lane > target_lane:



                    level[
                        source["id"]
                    ] = level[
                        target["id"]
                    ]







    # ==========================
    # 开始结束节点处理
    # ==========================

    def protect_start_end(
            self,
            data,
            level
    ):



        for node in data["nodes"]:



            # 开始固定顶部

            if node["type"] == "start":


                level[
                    node["id"]
                ] = 0





            # 结束不强制最后

            elif node["type"] == "end":


                if node["id"] not in level:


                    level[
                        node["id"]
                    ] = max(
                        level.values()
                    )





            else:



                # 普通节点不要和开始重叠

                if level[node["id"]] == 0:


                    level[
                        node["id"]
                    ] = 1







    # ==========================
    # 自动压缩空层
    # ==========================

    def compress_level(
            self,
            level
    ):



        used_levels = sorted(

            set(
                level.values()
            )

        )



        mapping = {


            old_level:new_level


            for new_level,old_level

            in enumerate(used_levels)


        }




        for node_id in level:


            level[node_id] = mapping[

                level[node_id]

            ]



        return level






    # ==========================
    # 计算最终坐标
    # ==========================

    def calculate(
            self,
            data
    ):



        # 计算基础层级

        level = self.calculate_level(
            data
        )



        # 跨泳道对齐

        self.align_cross_lane(
            data,
            level
        )



        # 开始结束约束

        self.protect_start_end(
            data,
            level
        )



        # 压缩空层

        self.compress_level(
            level
        )






        # 泳道索引

        lane_index = {}



        for i,lane in enumerate(data["lanes"]):


            lane_index[
                lane["id"]
            ] = i






        result = {}



        # 同泳道同层节点记录

        same_position_count = {}






        for node in data["nodes"]:



            # X 坐标

            x = (

                lane_index[
                    node["lane"]
                ]

                *

                self.lane_width

                +

                45

            )





            key = (

                node["lane"],

                level[node["id"]]

            )





            offset_index = same_position_count.get(

                key,

                0

            )



            same_position_count[key] = (

                offset_index + 1

            )





            # Y 坐标

            y = (

                level[
                    node["id"]
                ]

                *

                self.level_height

                +

                80

            )






            # 同泳道同层纵向避让

            if offset_index > 0:


                y += (

                    offset_index

                    *

                    self.same_level_offset

                )







            result[
                node["id"]
            ] = {


                "x": x,


                "y": y


            }





        return result