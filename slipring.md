graph TD
    %% 전체 스타일 정의
    classDef main fill:#f9f,stroke:#333,stroke-width:2px;
    classDef power fill:#e1f5fe,stroke:#0277bd,stroke-width:2px,stroke-dasharray: 5 5;
    classDef eth fill:#fff9c4,stroke:#fbc02d,stroke-width:2px;
    classDef frame fill:#eeeeee,stroke:#616161,stroke-width:1px;

    %% 1. 중공축 내부 삽입 방식
    subgraph Method1 [1. 중공축 내부 삽입 방식 (권장)]
        direction TB
        M1_Fixed[고정부 <br/> (크레인 마스트/지상)]
        M1_Rotating[회전부 <br/> (지브/운전석)]
        
        M1_Power_SR(大 전력 슬립링 <br/> Hollow Shaft형) -->|중심 축| M1_Center

        M1_Center{중심 빈 공간}
        
        %% 이더넷 슬립링 위치
        M1_Eth_SR[[小 이더넷 슬립링 <br/> (3.5cm)]]:::eth
        
        M1_Center -.->|내부 삽입| M1_Eth_SR
        
        M1_Eth_SR -.-> M1_Eth_Cable[이더넷 케이블]
        M1_Power_SR ==> M1_Power_Cable[전력 케이블]

        %% 스타일
        M1_Power_SR:::power
        M1_Fixed:::frame
        M1_Rotating:::frame
    end

    %% 2. 탠덤 (직렬 연결) 방식
    subgraph Method2 [2. 탠덤 (직렬 연결) 방식]
        direction TB
        M2_Fixed[고정부]
        M2_Rotating[회전부]

        M2_Power_SR(大 전력 슬립링) :::power
        
        M2_ShaftEnd(전력축 끝단)
        
        M2_Adapter[// 어댑터 브래킷 //]:::frame
        
        M2_Eth_SR[[小 이더넷 슬립링]]:::eth

        M2_Power_SR --- M2_ShaftEnd
        M2_ShaftEnd --- M2_Adapter
        M2_Adapter --- M2_Eth_SR
        
        M2_Fixed -.-> M2_AntiRot[회전 방지 핀] -.-> M2_Eth_SR
        
        M2_Power_SR ==> M2_Power_Cable[전력 케이블]
        M2_Eth_SR -.-> M2_Eth_Cable[이더넷 케이블]
        
        %% 스타일
        M2_Fixed:::frame
        M2_Rotating:::frame
    end

    %% 3. 사이드 마운트 및 벨트 구동 방식
    subgraph Method3 [3. 사이드 마운트 (벨트 구동) 방식]
        direction TB
        M3_Fixed[고정부]
        M3_Rotating[회전부]

        M3_MainShaft(메인 회전축):::power
        M3_Power_SR(大 전력 슬립링) :::power

        M3_Pulley1[대형 풀리]
        M3_Belt[== 타이밍 벨트 ==]
        M3_Pulley2[소형 풀리 (1:1)]
        
        M3_SubShaft(보조 회전축)
        M3_Eth_SR[[小 이더넷 슬립링]]:::eth

        M3_MainShaft --- M3_Pulley1
        M3_Pulley1 --- M3_Belt
        M3_Belt --- M3_Pulley2
        M3_Pulley2 --- M3_SubShaft
        M3_SubShaft --- M3_Eth_SR
        
        M3_Fixed --- M3_SubFrame[보조 프레임]:::frame --- M3_Eth_SR
        
        M3_Power_SR ==> M3_Power_Cable[전력 케이블]
        M3_Eth_SR -.-> M3_Eth_Cable[이더넷 케이블]
        
        %% 스타일
        M3_Fixed:::frame
        M3_Rotating:::frame
    end