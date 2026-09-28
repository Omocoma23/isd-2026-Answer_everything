\documentclass[12pt,a4paper]{article}
\usepackage{amsmath,amsfonts,graphicx}
\usepackage{tikz}%&lt;&lt;&lt;&lt;
\usetikzlibrary {positioning}

\begin{document}

<table><tr><td></td><th colspan="3">18</th></tr><tr><td>06026213</td><td>ระบบข้อมูลมหัต<br/>BIG DATA SYSTEMS</td><td>3 (2-2-5)</td></tr><tr><td>06026214</td><td>โครงงานวิทยาการข้อมูลและการวิเคราะห์เชิงธุรกิจ 1<br/>PROJECT IN DATA SCIENCE AND BUSINESS ANALYTICS 1</td><td>3 (0-9-0)</td></tr><tr><td>06026215</td><td>โครงงานวิทยาการข้อมูลและการวิเคราะห์เชิงธุรกิจ 2<br/>PROJECT IN DATA SCIENCE AND BUSINESS ANALYTICS 2</td><td>3 (0-9-0)</td></tr><tr><th colspan="4">3) กลุ่มวิชาชีพเฉพาะด้าน</th></tr><tr><td>- กลุ่มวิทยาการข้อมูล</td><td>12</td><td>หน่วยกิต<br/>หน่วยกิต (บรรยาย-ปฏิบัติ-ศึกษาด้วยตนเอง)</td></tr><tr><td>06026216</td><td>รหัสวิชา ชื่อวิชา<br/>ปัญญาประดิษฐ์<br/>ARTIFICIAL INTELLIGENCE</td><td>3 (3-0-6)</td></tr><tr><td>06026217</td><td>การเรียนรู้ของเครื่อง<br/>MACHINE LEARNING</td><td>3 (3-0-6)</td></tr><tr><td>06026218</td><td>การเรียนรู้เชิงลึก<br/>DEEP LEARNING</td><td>3 (2-2-5)</td></tr><tr><td>06026219</td><td>การประมวลผลภาษาธรรมชาติ<br/>NATURAL LANGUAGE PROCESSING</td><td>3 (3-0-6)</td></tr><tr><td>06026220</td><td>การทำเหมืองข้อมูลกระบวนการ<br/>PROCESS MINING</td><td>3 (3-0-6)</td></tr><tr><td>06026221</td><td>การค้นคืนสารสนเทศ<br/>INFORMATION RETRIEVAL</td><td>3 (3-0-6)</td></tr><tr><td>06026222</td><td>คอมพิวเตอร์รีชัน<br/>COMPUTER VISION</td><td>3 (3-0-6)</td></tr><tr><td>06026223</td><td>การประมวลผลภาพ<br/>IMAGE PROCESSING</td><td>3 (3-0-6)</td></tr><tr><td>06026224</td><td>การแปลงข้อมูลและการรู้จำรูปภาพ<br/>IMAGE TRANSFORMATION AND RECOGNITION</td><td>3 (3-0-6)</td></tr><tr><td>06026225</td><td>การเรียนรู้เชิงลึกสำหรับการวิเคราะห์ภาพและวีดีโอทางการ<br/>แพทย์<br/>DEEP LEARNING IN MEDICAL IMAGE AND VIDEO ANALYSIS</td><td>3 (2-2-5)</td></tr><tr><td>06026226</td><td>หัวข้อพิเศษทางวิทยาการข้อมูล 1<br/>SPECIAL TOPICS IN DATA SCIENCE 1</td><td>3 (3-0-6)</td></tr></table>

วท.บ (วิทยาการข้อมูลและการวิเคราะห์เชิงธุรกิจ) สาขาวิชาวิทยาการข้อมูลและการวิเคราะห์เชิงธุรกิจ
คณะเทคโนโลยีสารสนเทศ สจล.
\end{document}

---

\documentclass[12pt,a4paper]{article}
\usepackage{amsmath,amsfonts,graphicx,latexsym,color}
\usepackage{tikz}%&lt;&lt;&lt;&lt;&lt;
\tikzset{
    % TikZ code for the table header
    \tableheaderstyle/.append style={
        font={sffamily},
        align=center,
        draw=black!80,
        text width=4em,
        inner sep=1pt,
        outer sep=2pt,
    },
    % TikZ code for the table body
    \trbodystyle/.append style={
        font={sffamily},
        align=center,
        draw=black!80,
        text width=4em,
        inner sep=1pt,
        outer sep=2pt,
    },
}
\usepackage{tikz-cd}

% TikZ code for the table header
\begin{document}
  \begin{table}[h]
      \caption{\small รหัสวิชา,ชื่อวิชา,หน่วยกิต (บรรยาย-ปฏิบัติ-ศึกษาด้วยตนเอง),รายละเอียดการเรียนรู้และผลสัมฤทธิ์ที่ได้จากการทำกิจกรรมในห้องปฏิบัติการคอมพิวเตอร์ ภาคที่ 1 ปีการศึกษานี้ (2-2-5) \n รหัสวิชา: 06026227, 06026228, 06026229.} %\caption{\small รหัสวิชา,ชื่อวิชา,หน่วยกิต (บรรยาย-ปฏิบัติ-ศึกษาด้วยตนเอง),รายละเอียดการเรียนรู้และผลสัมฤทธิ์ที่ได้จากการทำกิจกรรมในห้องปฏิบัติการคอมพิวเตอร์ ภาคที่ 2 ปีการศึกษานี้ (3-0-6) \n รหัสวิชา: 06026230, 06026231, 06026232, 06026233, 06026234, 06026235, 06026236.} %\caption{\small รหัสวิชา,ชื่อวิชา,หน่วยกิต (บรรยาย-ปฏิบัติ-ศึกษาด้วยตนเอง),รายละเอียดการเรียนรู้และผลสัมฤทธิ์ที่ได้จากการทำกิจกรรมในห้องปฏิบัติการคอมพิวเตอร์ ภาคที่ 3 ปีการศึกษานี้ (2-2-5) \n รหัสวิชา: 06026237, 06026238.} %\caption{\small รหัสวิชา,ชื่อวิชา,หน่วยกิต (บรรยาย-ปฏิบัติ-ศึกษาด้วยตนเอง),รายละเอียดการเรียนรู้และผลสัมฤทธิ์ที่ได้จากการทำกิจกรรมในห้องปฏิบัติการคอมพิวเตอร์ ภาคที่ 4 ปีการศึกษานี้ (3-0-6) \n รหัสวิชา: 06026240.} %\caption{\small รหัสวิชา,ชื่อวิชา,หน่วยกิต (บรรยาย-ปฏิบัติ-ศึกษาด้วยตนเอง),รายละเอียดการเรียนรู้และผลสัมฤทธิ์ที่ได้จากการทำกิจกรรมในห้องปฏิบัติการคอมพิวเตอร์ ภาคที่ 5 ปีการศึกษานี้ (3-0-6) \n รหัสวิชา: 06026241.} %\caption{\small รหัสวิชา,ชื่อวิชา,หน่วยกิต (บรรยาย-ปฏิบัติ-ศึกษาด้วยตนเอง),รายละเอียดการเรียนรู้และผลสัมฤทธิ์ที่ได้จากการทำกิจกรรมในห้องปฏิบัติการคอมพิวเตอร์ ภาคที่ 6 ปีการศึกษานี้ (3-0-6) \n รหัสวิชา: 06026242.} %\caption{\small รหัสวิชา,ชื่อวิชา,หน่วยกิต (บรรยาย-ปฏิบัติ-ศึกษาด้วยตนเอง),รายละเอียดการเรียนรู้และผลสัมฤทธิ์ที่ได้จากการทำกิจกรรมในห้องปฏิบัติการคอมพิวเตอร์ ภาคที่ 7 ปีการศึกษานี้ (3-0-6) \n รหัสวิชา: 06026243.} %\caption{\small รหัสวิชา,ชื่อวิชา,หน่วยกิต (บรรยาย-ปฏิบัติ-ศึกษาด้วยตนเอง),รายละเอียดการเรียนรู้และผลสัมฤทธิ์ที่ได้จากการทำกิจกรรมในห้องปฏิบัติการคอมพิวเตอร์ ภาคที่ 8 ปีการศึกษานี้ (3-0-6) \n รหัสวิชา: 06026244.} %\caption{\small รหัสวิชา,ชื่อวิชา,หน่วยกิต (บรรยาย-ปฏิบัติ-ศึกษาด้วยตนเอง),รายละเอียดการเรียนรู้และผลสัมฤทธิ์ที่ได้จากการทำกิจกรรมในห้องปฏิบัติการคอมพิวเตอร์ ภาคที่ 9 ปีการศึกษานี้ (3-0-6) \n รหัสวิชา: 06026245.} %\caption{\small รหัสวิชา,ชื่อวิชา,หน่วยกิต (บรรยาย-ปฏิบัติ-ศึกษาด้วยตนเอง),รายละเอียดการเรียนรู้และผลสัมฤทธิ์ที่ได้จากการทำกิจกรรมในห้องปฏิบัติการคอมพิวเตอร์ ภาคที่ 10 ปีการศึกษานี้ (3-0-6) \n รหัสวิชา: 06026246.} %\caption{\small รหัสวิชา,ชื่อวิชา,หน่วยกิต (บรรยาย-ปฏิบัติ-ศึกษาด้วยตนเอง),รายละเอียดการเรียนรู้และผลสัมฤทธิ์ที่ได้จากการทำกิจกรรมในห้องปฏิบัติการคอมพิวเตอร์ ภาคที่ 11 ปีการศึกษานี้ (3-0-6) \n รหัสวิชา: 06026247.} %\caption{\small รหัสวิชา,ชื่อวิชา,หน่วยกิต (บรรยาย-ปฏิบัติ-ศึกษาด้วยตนเอง),รายละเอียดการเรียนรู้และผลสัมฤทธิ์ที่ได้จากการทำกิจกรรมในห้องปฏิบัติการคอมพิวเตอร์ ภาคที่ 12 ปีการศึกษานี้ (3-0-6) \n รหัสวิชา: 06026248.} %\caption{\small รหัสวิชา,ชื่อวิชา,หน่วยกิต (บรรยาย-ปฏิบัติ-ศึกษาด้วยตนเอง),รายละเอียดการเรียนรู้และผลสัมฤทธิ์ที่ได้จากการทำกิจกรรมในห้องปฏิบัติการคอมพิวเตอร์ ภาคที่ 13 ปีการศึกษานี้ (2-2-5) \n รหัสวิชา: 06026249.} %\caption{\small รหัสวิชา,ชื่อวิชา,หน่วยกิต (บรรยาย-ปฏิบัติ-ศึกษาด้วยตนเอง),รายละเอียดการเรียนรู้และผลสัมฤทธิ์ที่ได้จากการทำกิจกรรมในห้องปฏิบัติการคอมพิวเตอร์ ภาคที่ 14 ปีการศึกษานี้ (2-2-5) \n รหัสวิชา: 06026250.} %\caption{\small รหัสวิชา,ชื่อวิชา,หน่วยกิต (บรรยาย-ปฏิบัติ-ศึกษาด้วยตนเอง),รายละเอียดการเรียนรู้และผลสัมฤทธิ์ที่ได้จากการทำกิจกรรมในห้องปฏิบัติการคอมพิวเตอร์ ภาคที่ 15 ปีการศึกษานี้ (2-2-5) \n รหัสวิชา: 06026251.} %\caption{\small รหัสวิชา,ชื่อวิชา,หน่วยกิต (บรรยาย-ปฏิบัติ-ศึกษาด้วยตนเอง),รายละเอียดการเรียนรู้และผลสัมฤทธิ์ที่ได้จากการทำกิจกรรมในห้องปฏิบัติการคอมพิวเตอร์ ภาคที่ 16 ปีการศึกษานี้ (2-2-5) \n รหัสวิชา: 06026252.} %\caption{\small รหัสวิชา,ชื่อวิชา,หน่วยกิต (บรรยาย-ปฏิบัติ-ศึกษาด้วยตนเอง),รายละเอียดการเรียนรู้และผลสัมฤทธิ์ที่ได้จากการทำกิจกรรมในห้องปฏิบัติการคอมพิวเตอร์ ภาคที่ 17 ปีการศึกษานี้ (2-2-5) \n รหัสวิชา: 06026253.} %\caption{\small รหัสวิชา,ชื่อวิชา,หน่วยกิต (บรรยาย-ปฏิบัติ-ศึกษาด้วยตนเอง),รายละเอียดการเรียนรู้และผลสัมฤทธิ์ที่ได้จากการทำกิจกรรมในห้องปฏิบัติการคอมพิวเตอร์ ภาคที่ 18 ปีการศึกษานี้ (2-2-5) \n รหัสวิชา: 06026254.} %\caption{\small รหัสวิชา,ชื่อวิชา,หน่วยกิต (บรรยาย-ปฏิบัติ-ศึกษาด้วยตนเอง),รายละเอียดการเรียนรู้และผลสัมฤทธิ์ที่ได้จากการทำกิจกรรมในห้องปฏิบัติการคอมพิวเตอร์ ภาคที่ 19 ปีการศึกษานี้ (2-2-5) \n รหัสวิชา: 06026255.} %\caption{\small รหัสวิชา,ชื่อวิชา,หน่วยกิต (บรรยาย-ปฏิบัติ-ศึกษาด้วยตนเอง),รายละเอียดการเรียนรู้และผลสัมฤทธิ์ที่ได้จากการทำกิจกรรมในห้องปฏิบัติการคอมพิวเตอร์ ภาคที่ 20 ปีการศึกษานี้ (3-0-6) \n รหัสวิชา: 06026256.} %\caption{\small รหัสวิชา,ชื่อวิชา,หน่วยกิต (บรรยาย-ปฏิบัติ-ศึกษาด้วยตนเอง),รายละเอียดการเรียนรู้และผลสัมฤทธิ์ที่ได้จากการทำกิจกรรมในห้องปฏิบัติการคอมพิวเตอร์ ภาคที่ 21 ปีการศึกษานี้ (3-0-6) \n รหัสวิชา: 06026257.} %\caption{\small รหัสวิชา,ชื่อวิชา,หน่วยกิต (บรรยาย-ปฏิบัติ-ศึกษาด้วยตนเอง),รายละเอียดการเรียนรู้และผลสัมฤทธิ์ที่ได้จากการทำกิจกรรมในห้องปฏิบัติการคอมพิวเตอร์ ภาคที่ 22 ปีการศึกษานี้ (3-0-6) \n รหัสวิชา: 06026258.} %\caption{\small รหัสวิชา,ชื่อวิชา,หน่วยกิต (บรรยาย-ปฏิบัติ-ศึกษาด้วยตนเอง),รายละเอียดการเรียนรู้และผลสัมฤทธิ์ที่ได้จากการทำกิจกรรมในห้องปฏิบัติการคอมพิวเตอร์ ภาคที่ 23 ปีการศึกษานี้ (3-0-6) \n รหัสวิชา: 06026259.} %\caption{\small รหัสวิชา,ชื่อวิชา,หน่วยกิต (บรรยาย-ปฏิบัติ-ศึกษาด้วยตนเอง),รายละเอียดการเรียนรู้และผลสัมฤทธิ์ที่ได้จากการทำกิจกรรมในห้องปฏิบัติการคอมพิวเตอร์ ภาคที่ 24 ปีการศึกษานี้ (3-0-6) \n รหัสวิชา: 06026260.} %\caption{\small รหัสวิชา,ชื่อวิชา,หน่วยกิต (บรรยาย-ปฏิบัติ-ศึกษาด้วยตนเอง),รายละเอียดการเรียนรู้และผลสัมฤทธิ์ที่ได้จากการทำกิจกรรมในห้องปฏิบัติการคอมพิวเตอร์ ภาคที่ 25 ปีการศึกษานี้ (3-0-6) \n รหัสวิชา: 06026261.} %\caption{\small รหัสวิชา,ชื่อวิชา,หน่วยกิต (บรรยาย-ปฏิบัติ-ศึกษาด้วยตนเอง),รายละเอียดการเรียนรู้และผลสัมฤทธิ์ที่ได้จากการทำกิจกรรมในห้องปฏิบัติการคอมพิวเตอร์ ภาคที่ 26 ปีการศึกษานี้ (3-0-6) \n รหัสวิชา: 06026262.} %\caption{\small รหัสวิชา,ชื่อวิชา,หน่วยกิต (บรรยาย-ปฏิบัติ-ศึกษาด้วยตนเอง),รายละเอียดการเรียนรู้และผลสัมฤทธิ์ที่ได้จากการทำกิจกรรมในห้องปฏิบัติการคอมพิวเตอร์ ภาคที่ 27 ปีการศึกษานี้ (3-0-6) \n รหัสวิชา: 06026263.} %\caption{\small รหัสวิชา,ชื่อวิชา,หน่วยกิต (บรรยาย-ปฏิบัติ-ศึกษาด้วยตนเอง),รายละเอียดการเรียนรู้และผลสัมฤทธิ์ที่ได้จากการทำกิจกรรมในห้องปฏิบัติการคอมพิวเตอร์ ภาคที่ 28 ปีการศึกษานี้ (3-0-6) \n รหัสวิชา: 06026264.} %\caption{\small รหัสวิชา,ชื่อวิชา,หน่วยกิต (บรรยาย-ปฏิบัติ-ศึกษาด้วยตนเอง),รายละเอียดการเรียนรู้และผลสัมฤทธิ์ที่ได้จากการทำกิจกรรมในห้องปฏิบัติการคอมพิวเตอร์ ภาคที่ 29 ปีการศึกษานี้ (3-0-6) \n รหัสวิชา: 06026265.} %\caption{\small รหัสวิชา,ชื่อวิชา,หน่วยกิต (บรรยาย-ปฏิบัติ-ศ

---

\documentclass[12pt,a4paper]{article}
\usepackage{amsmath,amsfonts,graphicx,latexsym,color}
\usepackage{tikz}%&lt;&lt;&lt;&lt;&lt;&lt;
\tikzset{
    % TikZ code for the table header
    \tableheader[draw] [top center] [text width=4em]{#1};
}

% Table format: | Column 1 | Column 2 |
%|---|---|
%| Data 1| Data 2|

\begin{document}
    
    % TikZ code for the table
    \table[draw, 
        every node/.append style={draw}]
    {
        \tr[
            \td[width=0.5*\linewidth]{Data 1}%
            \td[width=0.5*\linewidth]{Data 2}%
        ]
    }
    
\end{document}

4) กลุ่มวิชาการศึกษาทางเลือก
6 หน่วยกิต

สำหรับแผนการศึกษาที่ไม่เข้าร่วมโครงการสหกิจศึกษา
- กลุ่มวิชาเลือก
6 หน่วยกิต

<table><tr><td>รหัสวิชา</td><td>ชื่อวิชา</td><td>หน่วยกิต (บรรยาย-ปฏิบัติ-ศึกษาด้วยตนเอง)</td></tr><tr><td>06026250</td><td>วิทยาการข้อมูลสำหรับธุรกิจ</td><td>3 (2-2-5)</td></tr><tr><td colspan="3">DATA SCIENCE FOR BUSINESS</td></tr><tr><td>06026251</td><td>บัญชีการเงิน</td><td>3 (3-0-6)</td></tr><tr><td colspan="3">FINANCIAL ACCOUNTING</td></tr><tr><td>06026252</td><td>การวิเคราะห์ด้านการเงิน</td><td>3 (2-2-5)</td></tr><tr><td colspan="3">FINANCIAL ANALYTICS</td></tr><tr><td>06026253</td><td>การวิเคราะห์ด้านการตลาด</td><td>3 (2-2-5)</td></tr><tr><td colspan="3">MARKETING ANALYTICS</td></tr><tr><td>06026254</td><td>เทคโนโลยีสุขภาพสนเทศศาสตร์เบื้องต้น</td><td>3 (2-2-5)</td></tr><tr><td colspan="3">INTRODUCTION TO HEALTH ANALYTICS</td></tr></table>

มคอ. 2
06026241 การดำเนินงานการเรียนรู้ของเครื่อง
MACHINE LEARNING OPERATIONS
3 (3-0-6)
06026242 โครงสร้างพื้นฐานด้านเทคโนโลยีกลุ่มเมฆ
CLOUD TECHNOLOGY INFRASTRUCTURE
3 (3-0-6)
06026243 ระบบฐานข้อมูลขั้นสูง
ADVANCED DATABASE SYSTEMS
3 (3-0-6)
06026244 การดูแลและบำรุงรักษาระบบฐานข้อมูล
DATABASE SYSTEM MAINTENANCE AND ADMINISTRATION
3 (2-2-5)
06026245 ระบบฐานข้อมูลแบบกระจาย
DISTRIBUTED DATABASE SYSTEMS
3 (3-0-6)
06026246 หัวข้อพิเศษทางวิศวกรรมข้อมูล 1
SPECIAL TOPICS IN DATA ENGINEERING 1
3 (3-0-6)
06026247 หัวข้อพิเศษทางวิศวกรรมข้อมูล 2
SPECIAL TOPICS IN DATA ENGINEERING 2
3 (3-0-6)
06026248 ปฏิบัติการพิเศษทางวิศวกรรมข้อมูล 1
SPECIAL WORKSHOP IN DATA ENGINEERING 1
3 (2-2-5)
06026249 ปฏิบัติการพิเศษทางวิศวกรรมข้อมูล 2
SPECIAL WORKSHOP IN DATA ENGINEERING 2
3 (2-2-5)

วท.บ (วิทยาการข้อมูลและการวิเคราะห์เชิงธุรกิจ) สาขาวิชาวิทยาการข้อมูลและการวิเคราะห์เชิงธุรกิจ
คณะเทคโนโลยีสารสนเทศ สจล.
<page_number>20</page_number>

---

\documentclass[12pt,a4paper]{article}
usepackage{amsmath,amsfonts,graphicx,latexsym,color}
usepackage{tikz}%&lt;&lt;&lt;&lt;&lt;&lt;
usepackage{amssymb,amsmath,bm,caption,epsfig,latexsym,color,graphicx,tikz}
\usetikzlibrary {positioning}

% ข้อความที่จะปรากฏในส่วนหัวของหน้ากระดาษ
% \begin{document}
% ข้อความแรก
% \end{document}
% ข้อความที่จะปรากฏในส่วนท้ายของหน้ากระดาษ
\begin{document}

\begin{table}[h]
    \caption{ตารางรายวิชาและน้ำหนักการเรียนรู้สำหรับบัณฑิตหลังจบระดับปริญญาตรี สาขาวิชาวิทยาการข้อมูลและการวิเคราะห์เชิงธุรกิจ (ภาคส่งเสริม) คณะเทคโนโลยีสารสนเทศ สจล. ปีการศึกษา พ.ศ. 2560-2563}
    \label{table1}
    \begin{tr}
        <td>รหัสวิชา</td><td>ชื่อวิชา</td><td>น้ำหนัก (หน่วยกิต)</td></tr>
    \end{tr>
    \foreach\x[count=\i] in {06026255, 3(2-2-5), การได้มาและการจัดการข้อมูลทางด้านคลินิก}, 06026256, 3 (3-0-6), การจัดการการปฏิบัติการ, 06026257, 3(3-0-6), การบริหารเชิงกลยุทธ์และสมรรถนะของธุรกิจ, 06026258, 3 (3-0-6), การวิเคราะห์เครือข่ายสังคม, SOCIAL NETWORK ANALYSIS}
    \ifnum\i&gt;1
        <tr>
            <td>รหัสวิชา</td><td>ชื่อวิชา</td><td>น้ำหนัก (หน่วยกิต)</td></tr>
        </tr>\fi
    \end{table}

% ข้อความที่จะปรากฏในส่วนหัวของหน้ากระดาษ
\begin{document}
% ข้อความแรก
% \end{document}
% ข้อความที่จะปรากฏในส่วนท้ายของหน้ากระดาษ
\begin{document}

\begin{table}[h]
    \caption{ตารางรายวิชาและน้ำหนักการเรียนรู้สำหรับบัณฑิตหลังจบระดับปริญญาตรี สาขาวิชาวิทยาการข้อมูลและการวิเคราะห์เชิงธุรกิจ (ภาคส่งเสริม) คณะเทคโนโลยีสารสนเทศ สจล. ปีการศึกษา พ.ศ. 2560-2563}
    \label{table1}
    \begin{tr>
        <td>รหัสวิชา</td><td>ชื่อวิชา</td><td>น้ำหนัก (หน่วยกิต)</td></tr>
    \end{tr}
    \foreach\x[count=\i] in {06026259, 6(0-35-0), สหกิจศึกษาทางวิทยาการข้อมูลและการวิเคราะห์เชิงธุรกิจ, COOPERATIVE EDUCATION IN DATA SCIENCE AND BUSINESS ANALYTICS}, 06026260, 6 (0-35-0), สหกิจศึกษาต่างประเทศทางวิทยาการข้อมูลและการวิเคราะห์เชิงธุรกิจ, OVERSEAS COOPERATIVE EDUCATION IN DATA SCIENCE AND BUSINESS ANALYTICS}
    \ifnum\i&gt;1
        <tr>
            <td>รหัสวิชา</td><td>ชื่อวิชา</td><td>น้ำหนัก (หน่วยกิต)</td></tr>
        </tr>\fi
    \end{table}

% ข้อความที่จะปรากฏในส่วนหัวของหน้ากระดาษ
\begin{document}
% ข้อความแรก
% \end{document}
% ข้อความที่จะปรากฏในส่วนท้ายของหน้ากระดาษ
\begin{document}

\begin{table}[h]
    \caption{ตารางรายวิชาและน้ำหนักการเรียนรู้สำหรับบัณฑิตหลังจบระดับปริญญาตรี สาขาวิชาวิทยาการข้อมูลและการวิเคราะห์เชิงธุรกิจ (ภาคส่งเสริม) คณะเทคโนโลยีสารสนเทศ สจล. ปีการศึกษา พ.ศ. 2560-2563}
    \label{table1}
    \begin{tr>
        <td>รหัสวิชา</td><td>ชื่อวิชา</td><td>น้ำหนัก (หน่วยกิต)</td></tr>
    \end{tr}
    \foreach\x[count=\i] in {06026259, 6(0-35-0), สหกิจศึกษาทางวิทยาการข้อมูลและการวิเคราะห์เชิงธุรกิจ, COOPERATIVE EDUCATION IN DATA SCIENCE AND BUSINESS ANALYTICS}, 06026260, 6 (0-35-0), สหกิจศึกษาต่างประเทศทางวิทยาการข้อมูลและการวิเคราะห์เชิงธุรกิจ, OVERSEAS COOPERATIVE EDUCATION IN DATA SCIENCE AND BUSINESS ANALYTICS}
    \ifnum\i&gt;1
        <tr>
            <td>รหัสวิชา</td><td>ชื่อวิชา</td><td>น้ำหนัก (หน่วยกิต)</td></tr>
        </tr>\fi
    \end{table}

% ข้อความที่จะปรากฏในส่วนหัวของหน้ากระดาษ
\begin{document}
% ข้อความแรก
% \end{document}
% ข้อความที่จะปรากฏในส่วนท้ายของหน้ากระดาษ
\begin{document}

\begin{table}[h]
    \caption{ตารางรายวิชาและน้ำหนักการเรียนรู้สำหรับบัณฑิตหลังจบระดับปริญญาตรี สาขาวิชาวิทยาการข้อมูลและการวิเคราะห์เชิงธุรกิจ (ภาคส่งเสริม) คณะเทคโนโลยีสารสนเทศ สจล. ปีการศึกษา พ.ศ. 2560-2563}
    \label{table1}
    \begin{tr>
        <td>รหัสวิชา</td><td>ชื่อวิชา</td><td>น้ำหนัก (หน่วยกิต)</td></tr>
    \end{tr}
    \foreach\x[count=\i] in {06026259, 6(0-35-0), สหกิจศึกษาทางวิทยาการข้อมูลและการวิเคราะห์เชิงธุรกิจ, COOPERATIVE EDUCATION IN DATA SCIENCE AND BUSINESS ANALYTICS}, 06026260, 6 (0-35-0), สหกิจศึกษาต่างประเทศทางวิทยาการข้อมูลและการวิเคราะห์เชิงธุรกิจ, OVERSEAS COOPERATIVE EDUCATION IN DATA SCIENCE AND BUSINESS ANALYTICS}
    \ifnum\i&gt;1
        <tr>
            <td>รหัสวิชา</td><td>ชื่อวิชา</td><td>น้ำหนัก (หน่วยกิต)</td></tr>
        </tr>\fi
    \end{table}

% ข้อความที่จะปรากฏในส่วนหัวของหน้ากระดาษ
\begin{document}
% ข้อความแรก
% \end{document}
% ข้อความที่จะปรากฏในส่วนท้ายของหน้ากระดาษ
\begin{document}

\begin{table}[h]
    \caption{ตารางรายวิชาและน้ำหนักการเรียนรู้สำหรับบัณฑิตหลังจบระดับปริญญาตรี สาขาวิชาวิทยาการข้อมูลและการวิเคราะห์เชิงธุรกิจ (ภาคส่งเสริม) คณะเทคโนโลยีสารสนเทศ สจล. ปีการศึกษา พ.ศ. 2560-2563}
    \label{table1}
    \begin{tr>
        <td>รหัสวิชา</td><td>ชื่อวิชา</td><td>น้ำหนัก (หน่วยกิต)</td></tr>
    \end{tr}
    \foreach\x[count=\i] in {06026259, 6(0-35-0), สหกิจศึกษาทางวิทยาการข้อมูลและการวิเคราะห์เชิงธุรกิจ, COOPERATIVE EDUCATION IN DATA SCIENCE AND BUSINESS ANALYTICS}, 06026260, 6 (0-35-0), สหกิจศึกษาต่างประเทศทางวิทยาการข้อมูลและการวิเคราะห์เชิงธุรกิจ, OVERSEAS COOPERATIVE EDUCATION IN DATA SCIENCE AND BUSINESS ANALYTICS}
    \ifnum\i&gt;1
        <tr>
            <td>รหัสวิชา</td><td>ชื่อวิชา</td><td>น้ำหนัก (หน่วยกิต)</td></tr>
        </tr>\fi
    \end{table}

% ข้อความที่จะปรากฏในส่วนหัวของหน้ากระดาษ
\begin{document}
% ข้อความแรก
% \end{document}
% ข้อความที่จะปรากฏในส่วนท้ายของหน้ากระดาษ
\begin{document}

\begin{table}[h]
    \caption{ตารางรายวิชาและน้ำหนักการเรียนรู้สำหรับบัณฑิตหลังจบระดับปริญญาตรี สาขาวิชาวิทยาการข้อมูลและการวิเคราะห์เชิงธุรกิจ (ภาคส่งเสริม) คณะเทคโนโลยีสารสนเทศ สจล. ปีการศึกษา พ.ศ. 2560-2563}
    \label{table1}
    \begin{tr>
        <td>รหัสวิชา</td><td>ชื่อวิชา</td><td>น้ำหนัก (หน่วยกิต)</td></tr>
    \end{tr}
    \foreach\x[count=\i] in {06026259, 6(0-35-0), สหกิจศึกษาทางวิทยาการข้อมูลและการวิเคราะห์เชิงธุรกิจ, COOPERATIVE EDUCATION IN DATA SCIENCE AND BUSINESS ANALYTICS}, 06026260, 6 (0-35-0), สหกิจศึกษาต่างประเทศทางวิทยาการข้อมูลและการวิเคราะห์เชิงธุรกิจ, OVERSEAS COOPERATIVE EDUCATION IN DATA SCIENCE AND BUSINESS ANALYTICS}
    \ifnum\i&gt;1
        <tr>
            <td>รหัสวิชา</td><td>ชื่อวิชา</td><td>น้ำหนัก (หน่วยกิต)</td></tr>
        </tr>\fi
    \end{table}

% ข้อความที่จะปรากฏในส่วนหัวของหน้ากระดาษ
\begin{document}
% ข้อความแรก
% \end{document}
% ข้อความที่จะปรากฏในส่วนท้ายของหน้ากระดาษ
\begin{document}

\begin{table}[h]
    \caption{ตารางรายวิชาและน้ำหนักการเรียนรู้สำหรับบัณฑิตหลังจบระดับปริญญาตรี สาขาวิชาวิทยาการข้อมูลและการวิเคราะห์เชิงธุรกิจ (ภาคส่งเสริม) คณะเทคโนโลยีสารสนเทศ สจล. ปีการศึกษา พ.ศ. 2560-2563}
    \label{table1}
    \begin{tr>
        <td>รหัสวิชา</td><td>ชื่อวิชา</td><td>น้ำหนัก (หน่วยกิต)</td></tr>
    \end{tr}
    \foreach\x[count=\i] in {06026259, 6(0-35-0), สหกิจศึกษาทางวิทยาการข้อมูลและการวิเคราะห์เชิงธุรกิจ, COOPERATIVE EDUCATION IN DATA SCIENCE AND BUSINESS ANALYTICS}, 06026260, 6 (0-35-0), สหกิจศึกษาต่างประเทศทางวิทยาการข้อมูลและการวิเคราะห์เชิงธุรกิจ, OVERSEAS COOPERATIVE EDUCATION IN DATA SCIENCE AND BUSINESS ANALYTICS}
    \ifnum\i&gt;1
        <tr>
            <td>รหัสวิชา</td><td>ชื่อวิชา</td><td>น้ำหนัก (หน่วยกิต)</td></tr>
        </tr>\fi
    \end{table}

% ข้อความที่จะปรากฏในส่วนหัวของหน้ากระดาษ
\begin{document}
% ข้อความแรก
% \end{document}
% ข้อความที่จะปรากฏในส่วนท้ายของหน้ากระดาษ
\begin{document}

\begin{table}[h]
    \caption{ตารางรายวิชาและน้ำหนักการเรียนรู้สำหรับบัณฑิตหลังจบระดับปริญญาตรี สาขาวิชาวิทยาการข้อมูลและการวิเคราะห์เชิงธุรกิจ (ภาคส่งเสริม) คณะเทคโนโลยีสารสนเทศ สจล. ปีการศึกษา พ.ศ. 2560-2563}
    \label{table1}
    \begin{tr>
        <td>รหัสวิชา</td><td>ชื่อวิชา</td><td>น้ำหนัก (หน่วยกิต)</td></tr>
    \end{tr}
    \foreach\x[count=\i] in {06026259, 6(0-35-0), สหกิจศึกษาทางวิทยาการข้อมูลและการวิเคราะห์เชิงธุรกิจ, COOPERATIVE EDUCATION IN DATA SCIENCE AND BUSINESS ANALYTICS}, 06026260, 6 (0-35-0), สหกิจศึกษาต่างประเทศทางวิทยาการข้อมูลและการวิเคราะห์เชิงธุรกิจ, OVERSEAS COOPERATIVE EDUCATION IN DATA SCIENCE AND BUSINESS ANALYTICS}
    \ifnum\i&gt;1
        <tr>
            <td>รหัสวิชา</td><td>ชื่อวิชา</td><td>น้ำหนัก (หน่วยกิต)</td></tr>
        </tr>\fi
    \end{table}

% ข้อความที่จะปรากฏในส่วนหัวของหน้ากระดาษ
\begin{document}
% ข้อความแรก
% \end{document}
% ข้อความที่จะปรากฏในส่วนท้ายของหน้ากระดาษ
\begin{document}

\begin{table}[h]
    \caption{ตารางรายวิชาและน้ำหนักการเรียนรู้สำหรับบัณฑิตหลังจบระดับปริญญาตรี สาขาวิชาวิทยาการข้อมูลและการวิเคราะห์เชิงธุรกิจ (ภาคส่งเสริม) คณะเทคโนโลยีสารสนเทศ สจล. ปีการศึกษา พ.ศ. 2560-2563}
    \label{table1}
    \begin{tr>
        <td>รหัสวิชา</td><td>ชื่อวิชา</td><td>น้ำหนัก (หน่วยกิต)</td></tr>
    \end{tr}
    \foreach\x[count=\i] in {06026259, 6(0-35-0), สหกิจศึกษาทางวิทยาการข้อมูลและการวิเคราะห์เชิงธุรกิจ, COOPERATIVE EDUCATION IN DATA SCIENCE AND BUSINESS ANALYTICS}, 06026260, 6 (0-35-0), สหกิจศึกษาต่างประเทศทางวิทยาการข้อมูลและการวิเคราะห์เชิงธุรกิจ, OVERSEAS COOPERATIVE EDUCATION IN DATA SCIENCE AND BUSINESS ANALYTICS}
    \ifnum\i&gt;1
        <tr

---

\documentclass[12pt,a4paper]{article}
usepackage{amsmath,amsfonts,graphicx}

% mathematical formula package (amsmath)
% linear algebra package (ltxtra)

% set the number of decimal places in all math formulas to 3
\usepackage{amsmath,amssymb,latexsym,color}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx}

% mathematical formula package (amsmath)
% linear algebra package (ltxtra)

% set the number of decimal places in all math formulas to 3
\usepackage{amsmath,amssymb,latexsym,color}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx}

% mathematical formula package (amsmath)
% linear algebra package (ltxtra)

% set the number of decimal places in all math formulas to 3
\usepackage{amsmath,amssymb,latexsym,color}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx}

% mathematical formula package (amsmath)
% linear algebra package (ltxtra)

% set the number of decimal places in all math formulas to 3
\usepackage{amsmath,amssymb,latexsym,color}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx}

% mathematical formula package (amsmath)
% linear algebra package (ltxtra)

% set the number of decimal places in all math formulas to 3
\usepackage{amsmath,amssymb,latexsym,color}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx}

% mathematical formula package (amsmath)
% linear algebra package (ltxtra)

% set the number of decimal places in all math formulas to 3
\usepackage{amsmath,amssymb,latexsym,color}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx}

% mathematical formula package (amsmath)
% linear algebra package (ltxtra)

% set the number of decimal places in all math formulas to 3
\usepackage{amsmath,amssymb,latexsym,color}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx}

% mathematical formula package (amsmath)
% linear algebra package (ltxtra)

% set the number of decimal places in all math formulas to 3
\usepackage{amsmath,amssymb,latexsym,color}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx}

% mathematical formula package (amsmath)
% linear algebra package (ltxtra)

% set the number of decimal places in all math formulas to 3
\usepackage{amsmath,amssymb,latexsym,color}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx}

% mathematical formula package (amsmath)
% linear algebra package (ltxtra)

% set the number of decimal places in all math formulas to 3
\usepackage{amsmath,amssymb,latexsym,color}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx}

% mathematical formula package (amsmath)
% linear algebra package (ltxtra)

% set the number of decimal places in all math formulas to 3
\usepackage{amsmath,amssymb,latexsym,color}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx}

% mathematical formula package (amsmath)
% linear algebra package (ltxtra)

% set the number of decimal places in all math formulas to 3
\usepackage{amsmath,amssymb,latexsym,color}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx}

% mathematical formula package (amsmath)
% linear algebra package (ltxtra)

% set the number of decimal places in all math formulas to 3
\usepackage{amsmath,amssymb,latexsym,color}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx}

% mathematical formula package (amsmath)
% linear algebra package (ltxtra)

% set the number of decimal places in all math formulas to 3
\usepackage{amsmath,amssymb,latexsym,color}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx}

% mathematical formula package (amsmath)
% linear algebra package (ltxtra)

% set the number of decimal places in all math formulas to 3
\usepackage{amsmath,amssymb,latexsym,color}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx}

% mathematical formula package (amsmath)
% linear algebra package (ltxtra)

% set the number of decimal places in all math formulas to 3
\usepackage{amsmath,amssymb,latexsym,color}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx}

% mathematical formula package (amsmath)
% linear algebra package (ltxtra)

% set the number of decimal places in all math formulas to 3
\usepackage{amsmath,amssymb,latexsym,color}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx}

% mathematical formula package (amsmath)
% linear algebra package (ltxtra)

% set the number of decimal places in all math formulas to 3
\usepackage{amsmath,amssymb,latexsym,color}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx}

% mathematical formula package (amsmath)
% linear algebra package (ltxtra)

% set the number of decimal places in all math formulas to 3
\usepackage{amsmath,amssymb,latexsym,color}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx}

% mathematical formula package (amsmath)
% linear algebra package (ltxtra)

% set the number of decimal places in all math formulas to 3
\usepackage{amsmath,amssymb,latexsym,color}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx}

% mathematical formula package (amsmath)
% linear algebra package (ltxtra)

% set the number of decimal places in all math formulas to 3
\usepackage{amsmath,amssymb,latexsym,color}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx}

% mathematical formula package (amsmath)
% linear algebra package (ltxtra)

% set the number of decimal places in all math formulas to 3
\usepackage{amsmath,amssymb,latexsym,color}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx}

% mathematical formula package (amsmath)
% linear algebra package (ltxtra)

% set the number of decimal places in all math formulas to 3
\usepackage{amsmath,amssymb,latexsym,color}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx}

% mathematical formula package (amsmath)
% linear algebra package (ltxtra)

% set the number of decimal places in all math formulas to 3
\usepackage{amsmath,amssymb,latexsym,color}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx}

% mathematical formula package (amsmath)
% linear algebra package (ltxtra)

% set the number of decimal places in all math formulas to 3
\usepackage{amsmath,amssymb,latexsym,color}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx}

% mathematical formula package (amsmath)
% linear algebra package (ltxtra)

% set the number of decimal places in all math formulas to 3
\usepackage{amsmath,amssymb,latexsym,color}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx}

% mathematical formula package (amsmath)
% linear algebra package (ltxtra)

% set the number of decimal places in all math formulas to 3
\usepackage{amsmath,amssymb,latexsym,color}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx}

% mathematical formula package (amsmath)
% linear algebra package (ltxtra)

% set the number of decimal places in all math formulas to 3
\usepackage{amsmath,amssymb,latexsym,color}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx}

% mathematical formula package (amsmath)
% linear algebra package (ltxtra)

% set the number of decimal places in all math formulas to 3
\usepackage{amsmath,amssymb,latexsym,color}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx}

% mathematical formula package (amsmath)
% linear algebra package (ltxtra)

% set the number of decimal places in all math formulas to 3
\usepackage{amsmath,amssymb,latexsym,color}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx}

% mathematical formula package (amsmath)
% linear algebra package (ltxtra)

% set the number of decimal places in all math formulas to 3
\usepackage{amsmath,amssymb,latexsym,color}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx}

% mathematical formula package (amsmath)
% linear algebra package (ltxtra)

% set the number of decimal places in all math formulas to 3
\usepackage{amsmath,amssymb,latexsym,color}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx}

% mathematical formula package (amsmath)
% linear algebra package (ltxtra)

% set the number of decimal places in all math formulas to 3
\usepackage{amsmath,amssymb,latexsym,color}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx}

% mathematical formula package (amsmath)
% linear algebra package (ltxtra)

% set the number of decimal places in all math formulas to 3
\usepackage{amsmath,amssymb,latexsym,color}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx}

% mathematical formula package (amsmath)
% linear algebra package (ltxtra)

% set the number of decimal places in all math formulas to 3
\usepackage{amsmath,amssymb,latexsym,color}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx}

% mathematical formula package (amsmath)
% linear algebra package (ltxtra)

% set the number of decimal places in all math formulas to 3
\usepackage{amsmath,amssymb,latexsym,color}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx}

% mathematical formula package (amsmath)
% linear algebra package (ltxtra)

% set the number of decimal places in all math formulas to 3
\usepackage{amsmath,amssymb,latexsym,color}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx}

% mathematical formula package (amsmath)
% linear algebra package (ltxtra)

% set the number of decimal places in all math formulas to 3
\usepackage{amsmath,amssymb,latexsym,color}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx}

% mathematical formula package (amsmath)
% linear algebra package (ltxtra)

% set the number of decimal places in all math formulas to 3
\usepackage{amsmath,amssymb,latexsym,color}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx}

% mathematical formula package (amsmath)
% linear algebra package (ltxtra)

% set the number of decimal places in all math formulas to 3
\usepackage{amsmath,amssymb,latexsym,color}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx}

% mathematical formula package (amsmath)
% linear algebra package (ltxtra)

% set the number of decimal places in all math formulas to 3
\usepackage{amsmath,amssymb,latexsym,color}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx}

% mathematical formula package (amsmath)
% linear algebra package (ltxtra)

% set the number of decimal places in all math formulas to 3
\usepackage{amsmath,amssymb,latexsym,color}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx}

% mathematical formula package (amsmath)
% linear algebra package (ltxtra)

% set the number of decimal places in all math formulas to 3
\usepackage{amsmath,amssymb,latexsym,color}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx}

% mathematical formula package (amsmath)
% linear algebra package (ltxtra)

% set the number of decimal places in all math formulas to 3
\usepackage{amsmath,amssymb,latexsym,color}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx}

% mathematical formula package (amsmath)
% linear algebra package (ltxtra)

% set the number of decimal places in all math formulas to 3
\usepackage{amsmath,amssymb,latexsym,color}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx}

% mathematical formula package (amsmath)
% linear algebra package (ltxtra)

% set the number of decimal places in all math formulas to 3
\usepackage{amsmath,amssymb,latexsym,color}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx}

% mathematical formula package (amsmath)
% linear algebra package (ltxtra)

% set the number of decimal places in all math formulas to 3
\usepackage{amsmath,amssymb,latexsym,color}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx}

% mathematical formula package (amsmath)
% linear algebra package (ltxtra)

% set the number of decimal places in all math formulas to 3
\usepackage{amsmath,amssymb,latexsym,color}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx}

% mathematical formula package (amsmath)
% linear algebra package (ltxtra)

% set the number of decimal places in all math formulas to 3
\usepackage{amsmath,amssymb,latexsym,color}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx}

% mathematical formula package (amsmath)
% linear algebra package (ltxtra)

% set the number of decimal places in all math formulas to 3
\usepackage{amsmath,amssymb,latexsym,color}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx}

% mathematical formula package (amsmath)
% linear algebra package (ltxtra)

% set the number of decimal places in all math formulas to 3
\usepackage{amsmath,amssymb,latexsym,color}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx}

% mathematical formula package (amsmath)
% linear algebra package (ltxtra)

% set the number of decimal places in all math formulas to 3
\usepackage{amsmath,amssymb,latexsym,color}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx}

% mathematical formula package (amsmath)
% linear algebra package (ltxtra)

% set the number of decimal places in all math formulas to 3
\usepackage{amsmath,amssymb,latexsym,color}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx}

% mathematical formula package (amsmath)
% linear algebra package (ltxtra)

% set the number of decimal places in all math formulas to 3
\usepackage{amsmath,amssymb,latexsym,color}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx}

% mathematical formula package (amsmath)
% linear algebra package (ltxtra)

% set the number of decimal places in all math formulas to 3
\usepackage{amsmath,amssymb,latexsym,color}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx}

% mathematical formula package (amsmath)
% linear algebra package (ltxtra)

% set the number of decimal places in all math formulas to 3
\usepackage{amsmath,amssymb,latexsym,color}
\usepackage[utf8

---

\documentclass[120mm]{a4paper}
\usepackage{amsmath,amsfonts,graphicx,latexsym,color}
\usepackage{tikz}%&lt;&lt;&lt;
%&lt;&lt;&lt; ตั้งค่าสีของเส้นที่ใช้ใน TikZ
\usetikzlibrary {positioning}

\tikzset{
    mynode/.append style={draw, align=center},
    tcancel/.append style={fill=#1!50, draw=black, inner sep=2pt},
    tcpgroup/.append style={fill=#1!75, fill opacity=0.8, above left of=tcancel, align=center},
}

\begin{document}
    
    \begin{table}[h]
        \caption{ปีที่ 1 ภาคการศึกษาที่ 2 มคอ. 2}
        \label{tab:1}
        \begin{tr}
            <td>รหัสวิชา</td>
            <td>ชื่อวิชา</td>
            <td>หน่วยกิต (บรรยาย-ปฏิบัติ-ศึกษาด้วยตนเอง)</td>
        </tr>
        \foreach\x[count=\i] in{06026201, แคลคูลัส 2 CALCULUS 2, 3 (3-0-6), \\06026203, การโปรแกรมคอมพิวเตอร์ COMPUTER PROGRAMMING, 3 (2-2-5), \\06026205, การตลาดเบื้องต้น INTRODUCTION TO MARKETING, 3 (3-0-6), \\06066001, ความน่าจะเป็นและสถิติ PROBABILITY AND STATISTICS, 3 (3-0-6), \\90641002, ความฉลาดทางดิจิทัล DIGITAL INTELLIGENCE QUOTIENT, 3 (3-0-6), \\90642033, กลุ่มวิชาที่กำหนดโดยคณะ* กฎหมายสำหรับคนรุ่นใหม่ LAW FOR NEW GENERATION, 3 (3-0-6), \\90644008, ภาษาอังกฤษพื้นฐาน 2 FOUNDATION ENGLISH 2, 3 (3-0-6)}{%
            \x
        }
    </table}
    
    <table><tr><td>รวม</td><td>21</td></tr></table>

วท.บ (วิทยาการข้อมูลและการวิเคราะห์เชิงธุรกิจ) สาขาวิชาวิทยาการข้อมูลและการวิเคราะห์เชิงธุรกิจ
คณะเทคโนโลยีสารสนเทศ สจล.
\end{document}

---

\documentclass[120mm]{a4paper}
\usepackage{amsmath,amsfonts,graphicx,latexsym,color}
\usepackage{tikz}%&lt;&lt;&lt;&lt;&lt;
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&

---

\documentclass[12pt,a4paper]{article}
usepackage{amsmath,amsfonts,graphicx,latexsym,color}
usepackage{tikz}%&lt;&lt;&lt;&lt;&lt;&lt;
usepackage{tikz-cd}

% TikZ code for the title page
\usetikzlibrary {positioning}

\begin{document}

    \begin{table}[h]
        \caption{ปีที่ 2 ภาคการศึกษาที่ 2}
        \label{tab1}
        \begin{tr}
            <td>รหัสวิชา</td>
            <td>ชื่อวิชา</td>
            <td>หน่วยกิต (บรรยาย-ปฏิบัติ-ศึกษาด้วยตนเอง)</td>
        </tr>
        \foreach\x[count=\i] in{06026204, 06026207, 06026208, 06026209, 06026210, 06066102, 06066301}{%
            \x
            <td>เครือข่ายและความมั่นคงทางไซเบอร์เบื้องต้น<br/>INTRODUCTION TO NETWORKS AND CYBERSECURITY</td>
            <td>$3$ (3-0-6)</td></tr><tr><td>06026207</td><td>ระบบฐานข้อมูลแบบโนเวสคิวแอล<br/>NOSQL DATABASE SYSTEMS</td><td>$3$ (2-2-5)</td></tr><tr><td>06026208</td><td>พื้นฐานวิทยาการข้อมูล<br/>FUNDAMENTALS OF DATA SCIENCE</td><td>$3$ (3-0-6)</td></tr><tr><td>06026209</td><td>การแสดงข้อมูลด้วยแผนภาพ<br/>DATA VISUALIZATION</td><td>$3$ (2-2-5)</td></tr><tr><td>06026210</td><td>การหาค่าที่เหมาะที่สุด<br/>OPTIMIZATION</td><td>$3$ (3-0-6)</td></tr><tr><td>06066102</td><td>ระบบสารสนเทศเพื่อการจัดการ<br/>MANAGEMENT INFORMATION SYSTEMS</td><td>$3$ (3-0-6)</td></tr><tr><td>06066301</td><td>โครงสร้างข้อมูลและอัลกอริทึม<br/>DATA STRUCTURES AND ALGORITHMS</td><td>$3$ (2-2-5)</td></tr><tr><td colspan="2">รวม</td><td>$21$</td></tr>
    \end{table}
    
    วท.บ (วิทยาการข้อมูลและการวิเคราะห์เชิงธุรกิจ) สาขาวิชาวิทยาการข้อมูลและการวิเคราะห์เชิงธุรกิจ
คณะเทคโนโลยีสารสนเทศ สจล.

\end{document}

---

\documentclass[120mm]{a4paper}
\usepackage{amsmath,amsfonts,graphicx,latexsym,color}
\usepackage{tikz}%&lt;&lt;&lt;&lt;&lt;&lt;
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz}%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt

---

\documentclass[12pt,a4paper]{article}
usepackage{amsmath,amsfonts,graphicx,latexsym,color}
usepackage{tikz}%&lt;&lt;&lt;&lt;&lt;&lt;
usepackage{color}

% set the background color of this page to light gray
\begin{document}
    \pagestyle{fancy}
    % set the text font to a sans-serif font
    \setfontfamily{serif}
    \usetikzlibrary {positioning,shapes,arrows,angles,decorations.pathmorphing}
    \usepackage[utf8]{inputenc}
    \usepackage{amsmath}
    \usepackage{amssymb}
    \usepackage{tikz}%&lt;&lt;&lt;&lt;&lt;&lt;
    % set the background color of this page to light gray
    \begin{document}

        \pagestyle{fancy}
        % set the text font to a sans-serif font
        \setfontfamily{serif}
        \usetikzlibrary {positioning,shapes,arrows,angles,decorations.pathmorphing}
        \usepackage[utf8]{inputenc}
        \usepackage{amsmath}
        \usepackage{amssymb}

    % set the background color of this page to light gray
    \end{document}
\end{tikzpicture}

---

Extract all text from the image.

Instructions:
- Only return the clean Markdown.
- Do not include any explanation or extra text.
- You must include all information on the page.

Formatting Rules:
- Tables: Render tables using <table>...</table> in clean HTML format.
- Equations: Render equations using LaTeX syntax with inline ($...$) and block ($$...$$).
- Images/Charts/Diagrams: Wrap any clearly defined visual areas (e.g. charts, diagrams, pictures) in:

<figure>
Describe the image’s main elements (people, objects, text), note any contextual clues (place, event, culture), mention visible text and its meaning, provide deeper analysis when relevant (especially for financial charts, graphs, or documents), comment on style or architecture if relevant, then give a concise overall summary. Describe in Thai.
</figure>


- Page Numbers: Wrap page numbers in <page_number>...</page_number> (e.g., <page_number>14</page_number>).
- Checkboxes: Use ☐ for unchecked and ☑ for checked boxes.
