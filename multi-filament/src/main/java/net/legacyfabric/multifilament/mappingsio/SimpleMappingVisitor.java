package net.legacyfabric.multifilament.mappingsio;

import java.io.IOException;
import java.util.List;
import java.util.Set;

import net.fabricmc.mappingio.MappedElementKind;
import net.fabricmc.mappingio.MappingFlag;
import net.fabricmc.mappingio.MappingVisitor;

public class SimpleMappingVisitor implements MappingVisitor {
	private final MappingVisitor parent;

	public SimpleMappingVisitor(MappingVisitor parent) {
		this.parent = parent;
	}

	@Override
	public Set<MappingFlag> getFlags() {
		return parent.getFlags();
	}

	@Override
	public void reset() {
		parent.reset();
	}

	@Override
	public boolean visitHeader() throws IOException {
		return parent.visitHeader();
	}

	@Override
	public void visitNamespaces(String srcNamespace, List<String> dstNamespaces) throws IOException {
		parent.visitNamespaces(srcNamespace, dstNamespaces);
	}

	@Override
	public void visitMetadata(String key, String value) throws IOException {
		parent.visitMetadata(key, value);
	}

	@Override
	public boolean visitContent() throws IOException {
		return parent.visitContent();
	}

	@Override
	public boolean visitClass(String srcName) throws IOException {
		return parent.visitClass(srcName);
	}

	@Override
	public boolean visitField(String srcName, String srcDesc) throws IOException {
		return parent.visitField(srcName, srcDesc);
	}

	@Override
	public boolean visitMethod(String srcName, String srcDesc) throws IOException {
		return parent.visitMethod(srcName, srcDesc);
	}

	@Override
	public boolean visitMethodArg(int argPosition, int lvIndex, String srcName) throws IOException {
		return parent.visitMethodArg(argPosition, lvIndex, srcName);
	}

	@Override
	public boolean visitMethodVar(int lvtRowIndex, int lvIndex, int startOpIdx, String srcName) throws IOException {
		return parent.visitMethodVar(lvtRowIndex, lvIndex, startOpIdx, srcName);
	}

	@Override
	public boolean visitEnd() throws IOException {
		return parent.visitEnd();
	}

	@Override
	public void visitDstName(MappedElementKind targetKind, int namespace, String name) throws IOException {
		parent.visitDstName(targetKind, namespace, name);
	}

	@Override
	public void visitDstDesc(MappedElementKind targetKind, int namespace, String desc) throws IOException {
		parent.visitDstDesc(targetKind, namespace, desc);
	}

	@Override
	public boolean visitElementContent(MappedElementKind targetKind) throws IOException {
		return parent.visitElementContent(targetKind);
	}

	@Override
	public void visitComment(MappedElementKind targetKind, String comment) throws IOException {
		parent.visitComment(targetKind, comment);
	}
}
