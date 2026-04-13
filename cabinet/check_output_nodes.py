#!/usr/bin/env python3
"""
Diagnostic script to check node count consistency across master layers in glide-circular.glyphs
Identifies glyphs with "Incompatible outlines" - where node counts differ across masters.
"""

import glyphsLib
from collections import defaultdict

def load_font():
    """Load the .glyphs file."""
    font = glyphsLib.load('glide-circular.glyphs')
    return font

def get_master_ids(font):
    """Get the set of master layer IDs."""
    return {m.id for m in font.masters}

def get_master_name(font, master_id):
    """Get the friendly name for a master ID."""
    for m in font.masters:
        if m.id == master_id:
            return m.customName or f"Master {m.id[:8]}"
    return f"Unknown {master_id[:8]}"

def get_layer_info(layer, font):
    """Extract readable info about a layer."""
    master_name = get_master_name(font, layer.layerId)
    layer_name = getattr(layer, 'name', '(unnamed)')
    
    # Count nodes per path/shape
    node_counts = []
    for shape in layer.shapes:
        if hasattr(shape, 'nodes'):
            # GSPath object
            node_counts.append(len(shape.nodes))
        else:
            # Likely a component
            node_counts.append('COMPONENT')
    
    return {
        'layer_id': layer.layerId,
        'is_master': layer.layerId in master_ids,
        'master_name': master_name,
        'layer_name': layer_name,
        'shape_count': len(layer.shapes),
        'node_counts': node_counts,
        'total_nodes': sum(n for n in node_counts if isinstance(n, int))
    }

def check_glyph_consistency(glyph, font):
    """
    Check if a glyph has consistent node counts across master layers.
    Returns (is_consistent, layer_infos, mismatches)
    """
    layer_infos = []
    master_node_patterns = {}  # master_name -> list of node counts
    
    for layer in glyph.layers:
        info = get_layer_info(layer, font)
        layer_infos.append(info)
        
        if info['is_master']:
            # For masters, track the pattern of node counts
            pattern = tuple(info['node_counts'])
            if pattern not in master_node_patterns.values():
                master_node_patterns[info['master_name']] = pattern
    
    # Check consistency: do all master layers have the same node count pattern?
    if len(master_node_patterns) > 1:
        # Multiple different patterns - inconsistent
        patterns = list(master_node_patterns.values())
        is_consistent = len(set(patterns)) == 1
    else:
        is_consistent = True
    
    return is_consistent, layer_infos, master_node_patterns

def report_failing_glyphs(font, failing_names):
    """Generate detailed report for the failing glyphs."""
    print("\n" + "="*80)
    print("FAILING GLYPHS DETAILED REPORT")
    print("="*80)
    
    incompatible_count = 0
    
    for glyph_name in sorted(failing_names):
        # Find glyph by name
        glyph = None
        for g in font.glyphs:
            if g.name == glyph_name:
                glyph = g
                break
        
        if glyph is None:
            print(f"\n[{glyph_name}] NOT FOUND in font")
            continue
        
        is_consistent, layer_infos, master_patterns = check_glyph_consistency(glyph, font)
        
        print(f"\n[{glyph_name}] Layers: {len(layer_infos)}")
        
        for info in layer_infos:
            marker = " (MASTER)" if info['is_master'] else " (EXTRA)"
            print(f"  {info['master_name']:15} | shapes={info['shape_count']:2} | nodes={info['node_counts']}{marker}")
        
        if not is_consistent:
            print(f"  >>> INCONSISTENT: Master layers have different node counts")
            for master_name, pattern in master_patterns.items():
                print(f"      {master_name}: {pattern}")
            incompatible_count += 1
        
        # Check for extra layers
        extra_count = sum(1 for info in layer_infos if not info['is_master'])
        if extra_count > 0:
            print(f"  WARNING: {extra_count} extra layer(s) beyond 4 masters")
    
    return incompatible_count

def scan_all_glyphs(font, master_ids):
    """Scan all glyphs for master layer inconsistencies."""
    print("\n" + "="*80)
    print("FULL FONT SCAN - ALL GLYPHS WITH INCONSISTENT MASTERS")
    print("="*80)
    
    incompatible_glyphs = []
    consistent_glyphs = []
    
    for glyph in font.glyphs:
        is_consistent, layer_infos, master_patterns = check_glyph_consistency(glyph, font)
        
        if not is_consistent:
            incompatible_glyphs.append((glyph.name, master_patterns, layer_infos))
        else:
            consistent_glyphs.append(glyph.name)
    
    print(f"\nTotal glyphs: {len(font.glyphs)}")
    print(f"Glyphs with CONSISTENT master layers: {len(consistent_glyphs)}")
    print(f"Glyphs with INCOMPATIBLE master layers: {len(incompatible_glyphs)}")
    
    if incompatible_glyphs:
        print(f"\nDetailed list of {len(incompatible_glyphs)} incompatible glyphs:")
        for glyph_name, patterns, layer_infos in sorted(incompatible_glyphs, key=lambda x: x[0]):
            print(f"\n  {glyph_name}:")
            for master_name, pattern in patterns.items():
                print(f"    {master_name}: {pattern}")
    
    return len(incompatible_glyphs), incompatible_glyphs

# Main execution
if __name__ == '__main__':
    print("Loading glide-circular.glyphs...")
    font = load_font()
    master_ids = get_master_ids(font)
    
    print(f"Font loaded: {len(font.glyphs)} glyphs, {len(font.masters)} masters")
    print(f"Master IDs: {[get_master_name(font, mid) for mid in master_ids]}")
    
    # Define failing glyphs from Glyphs.app errors
    failing_glyphs = [
        'Aring', 'Euro.tf', 'a.ss02', 'aacute.ss02', 'acircumflex.ss02',
        'adieresis.ss02', 'agrave.ss02', 'aring.ss02', 'atilde.ss02',
        'ccedilla', 'f_f.1', 'f_f_i.1', 'f_f_i', 'f_f_l.1', 'f_f_l', 'f_f',
        'fi.1', 'fi', 'f', 'oe', 'u.ordn', 'uacute', 'ucircumflex',
        'udieresis', 'ugrave', 'uni03BC.1', 'uni03BC', 'uniE000', 'uniE002', 'u'
    ]
    
    print(f"\nChecking {len(failing_glyphs)} failing glyphs from Glyphs.app errors...")
    
    # Report on failing glyphs
    failing_incompatible = report_failing_glyphs(font, failing_glyphs)
    
    # Scan all glyphs
    total_incompatible, all_incompatible = scan_all_glyphs(font, master_ids)
    
    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Failing glyphs from Glyphs.app that ARE incompatible: {failing_incompatible}/{len(failing_glyphs)}")
    print(f"Total glyphs with incompatible master layers: {total_incompatible}/{len(font.glyphs)}")
    print(f"\nROOT CAUSE: Node counts differ across master layers in these glyphs")
    print(f"SOLUTION: Ensure all master layers have identical outline structures")
