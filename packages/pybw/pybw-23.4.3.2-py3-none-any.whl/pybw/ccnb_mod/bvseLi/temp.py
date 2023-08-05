        
        
        
        
        bvs.Rmin_moveion = Rmin_moveion
        
        if len(bvs._Struct._OxidationTable) == 0:
            raise Exception('can not calculate BV and Ea without atom oxi info')
        
        bvs.stop = False
        
        centrepos = np.zeros(bvs._Size + [3])
        bvs.__Data['BVS'] = np.zeros(bvs._Size, dtype=np.double)
        bvs.__Data['BVSE'] = np.zeros(bvs._Size, dtype=np.double)
        bvs.__Data['BVEL'] = np.zeros(bvs._Size, dtype=np.double)
        
        for k in range(bvs._Size[2]):
            for j in range(bvs._Size[1]):
                for i in range(bvs._Size[0]):
                    centrepos[i][j][k][2] = k / (bvs._Size[2] - 1.0)
                    centrepos[i][j][k][1] = j / (bvs._Size[1] - 1.0)
                    centrepos[i][j][k][0] = i / (bvs._Size[0] - 1.0)
        
        if ProgressCall:
            ProgressCall(0)
        
        bvs._poss = bvs._Struct.FracPosToCartPos(centrepos)

        atomsq = {}
        for atom in bvs._Struct._atomsymbols:
            atomsq[atom] = 0
            for site in bvs._Struct._Sites:
                if atom in site.GetElements():
                    key = atom + str(site.GetElementsOxiValue()[atom])
                    atomsq[atom] = atomsq[atom] + site.GetElementsOxiValue()[atom] * site.GetElementsOccupy()[atom] / math.sqrt(bvs._Elementsparam[key][3])
        
        qsumanion = 0
        qsumcation = 0
        for (atom, value) in atomsq.items():
            if value > 0:
                qsumcation = qsumcation + value
            elif value < 0:
                qsumanion = qsumanion + value
            else:
                qsumanion = 0
                qsumcation = 0
        
        qsum = 0.0
        if bvs.ValenceOfMoveIon > 0:
            qsum = -qsumanion / qsumcation
        else:
            qsum = -qsumcation / qsumanion
        
        key1 = bvs._MoveIon + str(bvs.ValenceOfMoveIon)
        qm1 = bvs.ValenceOfMoveIon / math.sqrt(bvs._Elementsparam[key1][3])
        rm1 = bvs._Elementsparam[key1][6]
        
        for i in tqdm(range(bvs._Size[0])):
            (distance, neighborsindex) = bvs._Struct.GetKNeighbors(bvs._poss[i], kn=128)
            
            if ProgressCall:
                ProgressCall(10 + i * 90 / (bvs._Size[0] - 1))
            
            for j in range(bvs._Size[1]):
                
                for k in range(bvs._Size[2]):
                    if bvs.stop:
                        return False
                    
                    bvsdata = 0.0
                    data = 0.0
                    cdata = 0.0
                    bvelcdata = 0.0
                    N = 0
                    D0 = 0.0
                    Rcutoff = 10.0
                    alpha = 0.0
                    occupyvalue = 0.0
                    
                    for dindex, index in enumerate(neighborsindex[j][k]):
                        site2 = bvs._Struct._SuperCellusites[index]
                        
                        if site2.GetIronType() * bvs.ValenceOfMoveIon < 0:
                            for (ssymbol, occupyvalue) in site2.GetElementsOccupy().items():
                                if ssymbol != 'Vac':
                                    site2oxi = site2.GetElementsOxiValue()[ssymbol]
                                    if bvs.ValenceOfMoveIon > 0:
                                        key = "".join([bvs._MoveIon, str(bvs.ValenceOfMoveIon), ssymbol, str(site2oxi)])
                                    else:
                                        key = "".join([ssymbol, str(site2oxi), bvs._MoveIon, str(bvs.ValenceOfMoveIon)])
                                    if (key in bvs._BVSEparam) and (key in bvs._BVparam):
                                        (Nc, r0, Rcutoff, D0, Rmin, alpha) = bvs._BVSEparam[key][0]
                                        (r, b) = bvs._BVparam[key][0]
                                        Rcutoff = 10.0
                                        if distance[j][k][dindex] <= Rcutoff:
                                            # bv=np.exp((r0-distance[k][j][i][dindex])*alpha)
                                            _bvs = np.exp((r - distance[j][k][dindex]) / b)
                                            smin = np.exp((Rmin - distance[j][k][dindex]) * alpha)
                                            en_s = np.exp((Rmin - Rcutoff) * alpha)
                                            bvsdata = bvsdata + _bvs  #*occupyvalue-((en_s-1)**2-1)
                                            data = data + ((smin - 1)**2 - 1) * occupyvalue
                                    else:
                                        if (key not in bvs._BVSEparam):
                                            raise Exception("bvse {0}  param can't find!!!!".format(key))
                                            ProgressCall(0)
                                        else:
                                            raise Exception("_bvs {0} param can't find!!!!".format(key))
                                            ProgressCall(0)
                        else:
                            for (ssymbol, occupyvalue) in site2.GetElementsOccupy().items():
                                if ssymbol != 'Vac':
                                    site2oxi = site2.GetElementsOxiValue()[ssymbol]
                                    
                                    if ssymbol != bvs._MoveIon:
                                        key = ssymbol + str(site2oxi)
                                        rm2 = bvs._Elementsparam[key][6]
                                        qm2 = site2oxi / math.sqrt(bvs._Elementsparam[key][3])
                                        rm1m2 = distance[j][k][dindex]
                                        f = 0.74
                                        if rm1m2 > rm2:
                                            if rm1m2 < Rcutoff:
                                                cdata = cdata + occupyvalue * qm1 * qm2 / rm1m2 * erfc(rm1m2 / (f * (rm1 + rm2))) * qsum
                                                bvelcdata = bvelcdata + occupyvalue * qm1 * qm2 / rm1m2 * (erfc(rm1m2 / (f * (rm1 + rm2))) - erfc(Rcutoff / (f * (rm1 + rm2))))
                                        else:
                                            cdata = 300
                                            bvelcdata = 300
                                    
                                    elif ssymbol == bvs._MoveIon:
                                        key = ssymbol + str(site2oxi)
                                        rm2 = bvs._Elementsparam[key][6]
                                        qm2 = site2oxi / math.sqrt(bvs._Elementsparam[key][3])
                                        rm1m2 = distance[j][k][dindex]
                                        f = 0.74
                                        
                                        if rm1m2 > bvs.Rmin_moveion:
                                            if rm1m2 < Rcutoff:
                                                cdata = cdata + occupyvalue * qm1 * qm2 / rm1m2 * erfc(rm1m2 / (f * (rm1 + rm2))) * qsum
                                                bvelcdata = bvelcdata + occupyvalue * qm1 * qm2 / rm1m2 * (erfc(rm1m2 / (f * (rm1 + rm2))) - erfc(Rcutoff / (f * (rm1 + rm2))))
                                        else:
                                            cdata = cdata + 0
                                            bvelcdata = bvelcdata + 0