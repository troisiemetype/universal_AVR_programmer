#!/usr/bin/env python3

from kikit import panelize, substrate
from kikit.units import mm, deg
from kikit import panelize_ui_impl as ki
import shapely
import shapely.geometry
import pcbnew
import sys
import itertools

import ipdb


def main():
    pcb_filename = "../ISP.kicad_pcb"

    panel_filename = "ISP_panel.kicad_pcb"

    frame_width = 6 * mm
    rail_width = frame_width
    backbone_width = frame_width

    tab_width = 2 * mm
    backbone_cut_width = tab_width
    board_spacing = backbone_width + 2 * tab_width


    frame_hor_space = tab_width
    frame_ver_space = tab_width

    frame_hor_offset = tab_width
    frame_ver_offset = tab_width

    panel = panelize.Panel(panel_filename)

    # add the boards
    
    mainPcb_source_area = pcbnew.wxRect(
        pcbnew.wxPointMM(68, 47), pcbnew.wxPointMM(96, 113)
    )

    plug1Pcb_source_area = pcbnew.wxRect(
        pcbnew.wxPointMM(120, 50), pcbnew.wxPointMM(140, 80)
    )

    plug2Pcb_source_area = pcbnew.wxRect(
        pcbnew.wxPointMM(150, 50), pcbnew.wxPointMM(170, 80)
    )

    plug3Pcb_source_area = pcbnew.wxRect(
        pcbnew.wxPointMM(180, 50), pcbnew.wxPointMM(210, 80)
    )

    main_origin = pcbnew.wxPointMM(40, 60)

    bounding_box_1= panel.appendBoard(
        pcb_filename,
        destination = main_origin,
        sourceArea = mainPcb_source_area,
        shrink = True,
        rotationAngle = 0,
        origin = panelize.Origin.Center,
        tolerance = 10 * mm,
    )

    plug1Pcb_origin = pcbnew.wxPointMM(63, 45)

    bounding_box_2 = panel.appendBoard(
        pcb_filename,
        destination = plug1Pcb_origin,
        sourceArea = plug1Pcb_source_area,
        shrink = True,
        rotationAngle = -900,
        origin = panelize.Origin.Center,
        tolerance = 10 * mm,
    )

    plug2Pcb_origin = pcbnew.wxPointMM(60, 75)

    bounding_box_3 = panel.appendBoard(
        pcb_filename,
        destination = plug2Pcb_origin,
        sourceArea = plug2Pcb_source_area,
        shrink = True,
        rotationAngle = 1800,
        origin = panelize.Origin.Center,
        tolerance = 10 * mm,
    )

    plug3Pcb_origin = pcbnew.wxPointMM(63, 60)

    bounding_box_4 = panel.appendBoard(
        pcb_filename,
        destination = plug3Pcb_origin,
        sourceArea = plug3Pcb_source_area,
        shrink = True,
        rotationAngle = -900,
        origin = panelize.Origin.Center,
        tolerance = 10 * mm,
    )


    # add frame

    cuts = panel.makeFrame(frame_width, frame_hor_space, frame_ver_space)
#    cuts = panel.makeTightFrame(6, 3, 6, 6)
#    cuts = panel.makeRailsTb(6 * mm)

    # create a dummy framing substrate (required for partition lines)

    framing_substrates = ki.dummyFramingSubstrate(
        panel.substrates, (frame_width, frame_width)
    )
#    panel.debugRenderBoundingBoxes()

    panel.buildPartitionLineFromBB(framing_substrates)
#    panel.buildPartitionLineFromBB()
    
 #   panel.debugRenderPartitionLines()

#    panel.save()
#    return

    # add a backbone
    
#    backbone_cuts = []
    '''
    backbone_cuts = panel.renderBackbone(
        backbone_width, 0, backbone_cut_width, backbone_cut_width
    )
    '''
    frame_cuts = itertools.chain(*cuts)

    # add the tabs

    tab_cuts = panel.buildTabsFromAnnotations()

    # OR add rails

    # panel.makeRailsLr(rail_width)
    # frame_cuts = []

    panel.addMillFillets(1.0 * mm)

    panel.copperFillNonBoardAreas()
    
#    panel.debugRenderBackboneLines()
#    panel.debugRenderBoundingBoxes()
#    panel.debugRenderPartitionLines()

    # create the tab cuts

    panel.makeMouseBites(
        tab_cuts,
        diameter=0.5 * mm,
        spacing=0.75 * mm,
        offset=0.25 * mm,
        prolongation=0.5 * mm,
    )

    # create the backbone and frame cuts
    
    panel.makeMouseBites(
        itertools.chain(frame_cuts),
        diameter=0.5 * mm,
        spacing=0.75 * mm,
        offset=0.25 * mm,
        prolongation=0.5 * mm,
    )
    
    panel.save()


if __name__ == "__main__":
    main()
